# Nome: João Paulo Magiero
# https://youtu.be/dkKTeXxGx6A

import heapq
import os
import uuid


def merge_sort(array):
  if len(array) > 1:
    mid = len(array) // 2
    left_half = array[:mid]
    right_half = array[mid:]

    merge_sort(left_half)
    merge_sort(right_half)

    i = j = k = 0
    while i < len(left_half) and j < len(right_half):
      if left_half[i] < right_half[j]:
        array[k] = left_half[i]
        i += 1
      else:
        array[k] = right_half[j]
        j += 1
      k += 1

    while i < len(left_half):
      array[k] = left_half[i]
      i += 1
      k += 1

    while j < len(right_half):
      array[k] = right_half[j]
      j += 1
      k += 1

  return array


def write_temp_file(sorted_data):
  temp_file = f'temp_{uuid.uuid4()}.txt'
  with open(temp_file, 'w') as file:
    for line in sorted_data:
      file.write(line + '\n')
  return temp_file


def divide_and_sort(file_path, memory_limit):
  temp_files = []
  total_lines_read = 0
  buffer_size = memory_limit // 100

  with open(file_path, 'r') as file:
    while True:
      lines = [file.readline().strip() for _ in range(buffer_size)]
      lines = list(filter(None, lines))
      if not lines:
        break
      total_lines_read += len(lines)
      sorted_lines = merge_sort(lines)
      temp_file_path = write_temp_file(sorted_lines)
      temp_files.append(temp_file_path)

  return total_lines_read, temp_files


def k_way_merge(temp_files, output_file):

  total_lines_written = 0
  with open(output_file, 'w') as out_file:
    files = [open(file, 'r') for file in temp_files]
    heap = [(file.readline().strip(), idx) for idx, file in enumerate(files)]
    heapq.heapify(heap)

    while heap:
      smallest, file_idx = heapq.heappop(heap)
      if smallest:
        out_file.write(smallest + '\n')
        total_lines_written += 1
        next_element = files[file_idx].readline().strip()
        if next_element:
          heapq.heappush(heap, (next_element, file_idx))

    for file in files:
      file.close()

  return total_lines_written


def delete_temp_files(temp_files):
  for file in temp_files:
    os.remove(file)


def request_limit_memory():
  while True:
    try:
      memory_limit = float(input("Digite o limite de memória em MB: "))
      if memory_limit <= 0:
        print("Por favor, insira um valor positivo.")
      else:
        return int(memory_limit * 1024 * 1024)
    except ValueError:
      print("Entrada inválida. Por favor, digite um número.")


def external_merge_sort(file_path, output_file, memory_limit):
  total_lines_read, temp_files = divide_and_sort(file_path, memory_limit)
  total_lines_written = k_way_merge(temp_files, output_file)
  delete_temp_files(temp_files)

  return total_lines_read, total_lines_written


input_file = '1m.txt'
output_file = 'uuids_ordenados.txt'
memory_limit_mb = request_limit_memory()
total_lines_read, total_lines_written = external_merge_sort(
    input_file, output_file, memory_limit_mb)
print(f'Total lido: {total_lines_read}, Total escrito: {total_lines_written}')
