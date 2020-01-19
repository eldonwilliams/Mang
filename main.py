from time import sleep
from os import system
import os

var_stack = {}
function_stack = {}

def query(logic, i1, i2):
  if logic: return i1
  else: return i2

def get_poses(string, find):
  lead = 0
  counts = 0
  save_begin = 0
  for char in string:
    counts += 1
    if char == find[lead]:
      lead += 1
      if lead >= len(find):
        return [save_begin, counts]

def parse_program(program):
  code = []
  for line in program:
    if line == "": continue
    if line.startswith("//"): continue
    process = line
    if process[len(process)-1] == ";":
      code.append(process.split(";")[0])
    else:
      code.append(process)
  return code

def run_program(program):
  on_func = False
  func = ""
  for line in program:
    if line == "": continue
    if line.startswith("//"): continue
    prompt = line.split(" ")

    count = 0
    for prom in prompt:
      if "call::" in prom:
        prompt[count] = prompt[count].replace("call::", "")
        prompt[count] = var_stack[prompt[count]]
      elif "inp" == prom:
        prompt[count] = input()
      count += 1
      
    count = 0
    for prom in prompt:
      if "+" == prom:
        num = int(prompt[count + 1]) + int(prompt[count + 2])
        prompt.pop(count)
        prompt.pop(count)
        prompt[count] = str(num)
      elif "-" == prom:
        num = int(prompt[count + 1]) - int(prompt[count + 2])
        prompt.pop(count)
        prompt.pop(count)
        prompt[count] = str(num)
      elif "*" == prom:
        num = int(prompt[count + 1]) * int(prompt[count + 2])
        prompt.pop(count)
        prompt.pop(count)
        prompt[count] = str(num)
      elif "/" == prom:
        num = int(prompt[count + 1]) / int(prompt[count + 2])
        prompt.pop(count)
        prompt.pop(count)
        prompt[count] = str(num)

      count += 1

    if on_func == True:
      function_stack[func].append(line)
    else:
      if prompt[0] == "clr":
        system('cls' if os.name == 'nt' else 'clear')
      elif prompt[0] == "slp":
        sleep(int(prompt[1]))
      elif prompt[0] == "log":
        if len(prompt) >= 2:
          cnt = 0
          for arg in prompt:
            if cnt >= 2:
              prompt[1] += " " + prompt[cnt]
            cnt += 1
        print("> {}".format(prompt[1]))
      elif prompt[0] == "run":
        opend = open(prompt[1], 'r')
        program = []
        for line in opend.readlines():
          program.append(line.split("\n")[0])
        run_program(parse_program(program))
      elif prompt[0] == "var":
        name = prompt[1]
        var_stack[name] = ""
        prompt.pop(0)
        prompt.pop(0)
        loop = 0
        for thing in prompt:
          loop += 1
          var_stack[name] += thing + query(loop >= len(prompt), "", " ")
      elif prompt[0] == "rlod":
        system('cls' if os.name == 'nt' else 'clear')
        start_Mang()
      elif prompt[0] == "func":
        function_stack[prompt[1]] = []
        on_func = True
        func = prompt[1]
      elif prompt[0] == "call":
        function = function_stack[prompt[1]]
        run_program(parse_program(function))
      elif prompt[0] == "repeat":
        count = 0
        function = function_stack[prompt[2]]
        parsed = parse_program(function)
        while True:
          count += 1
          run_program(parsed)
          if count >= int(prompt[1]):break
      elif prompt[0] == "if":
        function = function_stack[prompt[4]]
        parsed = parse_program(function)
        if prompt[1] == "==" and prompt[2] == prompt[3]:
          run_program(parsed)
        elif prompt[1] == "!=" and prompt[2] != prompt[3]:
          run_program(parsed)
        

    if on_func and line[len(line)-1] == "|":
      on_func = False

def start_Mang():
  print("Mang 1.5 (Released)\n")
  print("[]\n\n")
  while True:
    code = input("|")
    if not code: continue
    if code[len(code)-1] == ";":
      code = [code.split(";")[0]]
      while True:
        new_line = input(".")
        if not new_line:
          break
        if new_line[len(new_line)-1] == ";":
          code.append(new_line.split(";")[0])
        else:
          code.append(new_line)
          break
    else:
      code = [code]


    run_program(code)

start_Mang()