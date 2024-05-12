import subprocess
import os

def archive_files(input_dir, output_dir, files_per_archive, verbose=False):
    # Получаем список всех файлов в указанной директории
    files = os.listdir(input_dir)
    files.sort()  # Сортируем файлы по алфавиту

    num_files = len(files)
    num_archives = num_files // files_per_archive + (1 if num_files % files_per_archive != 0 else 0)

    for i in range(num_archives):
        start_index = i * files_per_archive
        end_index = min((i + 1) * files_per_archive, num_files)
        archive_name = os.path.join(output_dir, f"scener_{i}.tar")

        # Формируем список файлов для текущего архива
        files_to_archive = [os.path.join(input_dir, file) for file in files[start_index:end_index]]

        # Выполняем команду tar для архивирования файлов
        subprocess.run(["tar", "-czvf" if verbose else "-czf", archive_name] + files_to_archive)
        print(f"Архив {archive_name} создан.")

if __name__ == "__main__":
    input_directory = "./scener_dataset"
    output_directory = "./archives"
    files_per_archive = 500

    archive_files(input_directory, output_directory, files_per_archive)
