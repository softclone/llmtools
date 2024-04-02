import os
import readline
from datetime import datetime
from pathlib import Path

async def prompt_user(question):
    return input(question)

async def select_files(current_dir, exclude_patterns):
    selected_files = []

    for file in os.listdir(current_dir):
        file_path = os.path.join(current_dir, file)
        if os.path.isdir(file_path):
            if file not in exclude_patterns:
                include_folder = await prompt_user(f"Include folder '{file}'? (y/n) ")
                if include_folder.lower() == 'y':
                    sub_files = await select_files(file_path, exclude_patterns)
                    selected_files.extend(sub_files)
        else:
            include_file = await prompt_user(f"Include file '{file}'? (y/n) ")
            if include_file.lower() == 'y':
                selected_files.append(file_path)

    return selected_files

async def merge_files(selected_files, output_file_path):
    merged_content = ''

    for file_path in selected_files:
        with open(file_path, 'r') as file:
            file_content = file.read()
            section_header = f"\n{file_path.upper()} CODE IS BELOW\n"
            merged_content += section_header + file_content + '\n'

    with open(output_file_path, 'w') as file:
        file.write(merged_content)

async def create_output_directory(output_dir_path):
    Path(output_dir_path).mkdir(parents=True, exist_ok=True)

def get_timestamped_file_name():
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    return f"merged-repo-{timestamp}.txt"

async def main():
    current_dir = os.getcwd()

    print('Select files and folders to include in the merge:')
    exclude_patterns = ['__pycache__']  # Add more patterns if needed
    selected_files = await select_files(current_dir, exclude_patterns)

    output_dir_name = 'llm_text_transcripts'
    output_dir_path = os.path.join(current_dir, output_dir_name)
    await create_output_directory(output_dir_path)

    output_file_name = get_timestamped_file_name()
    output_file_path = os.path.join(output_dir_path, output_file_name)
    await merge_files(selected_files, output_file_path)

    print(f"Merged repository saved to: {output_file_path}")

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())