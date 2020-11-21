import os
import sys
import json
import asyncio
import datetime
from request_validator import Validator


class JobsExecutor:
    def __init__(self, data):
        self._data = data
        self._res = {}

    def start_execution(self):
        jobs = self._data['jobs']

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._execute_jobs(jobs))
        loop.close()

    async def _execute_jobs(self, jobs):
        tasks = [asyncio.ensure_future(self._execute_job(job)) for job in jobs]
        await asyncio.wait(tasks)

    async def _execute_job(self, job):
        '''
        Запускает команды в джобе на исполнение.
        '''
        name = job['name']
        commands = job['commands']
        directory = job['result_directory']

        path = self._get_path(directory)

        with open(f'{path}\\{name}.log', 'w') as f:
            for cmd in commands:
                try:
                    code, stdout, stderr = await self._run_cmd(cmd)
                except UnicodeDecodeError:
                    self._res[name] = 'FAIL'
                    break

                self._write_log(f, cmd, code, stdout, stderr)

                if code != 0:
                    self._res[name] = 'FAIL'
                    break

                self._res[name] = 'OK'

    async def _run_cmd(self, cmd):
        '''
        Возвращает код завершения процесса, stdout и stderr.
        '''
        p = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await p.communicate()

        code = p.returncode
        format_out = stdout.decode().strip()
        format_err = stderr.decode().strip().replace('\r\n', '\n\t')

        return code, format_out, format_err

    def _write_log(self, f_out, cmd, code, stdout, stderr):
        '''
        Запись логов в файл.
        '''
        time = datetime.datetime.now()
        f_out.write(f'time: {time}\n')
        f_out.write(f'cmd: {cmd}\n')
        f_out.write(f'exitcode: {code}\n')

        if len(stdout) != 0:
            f_out.write(f'stdout:\n\t{stdout}\n\n')
        if len(stderr) != 0:
            f_out.write(f'stderr:\n\t{stderr}\n\n')

    def _get_path(self, path):
        '''
        Создает директорию, если ее не существует. 
        Возвращает абсолютный путь до конечной директории.
        '''
        # Если путь относительный
        if path[0] == r'/':
            parent_dir = os.getcwd()
            path = os.path.join(parent_dir, path[1:])
            if not os.path.isdir(path):
                os.makedirs(path)
        # Если путь абсолютный
        else:
            if not os.path.isdir(path):
                os.makedirs(path)
        return path

    def get_results(self):
        '''
        Возвращает результаты выполнения задач (dict).
        '''
        return self._res


def main(f_in):
    with open(f_in, "r") as f:
        try:
            data = json.load(f)
        except json.decoder.JSONDecodeError:
            return 'Invalid JSON'

        validator = Validator(data)
        # Проверка корректности входных данных
        if not validator.is_valid_data():
            # Если данные некорректные, то возвращается словарь с ошибкой
            return validator.get_res()

        res = {}
        exec_jobs = JobsExecutor(data)
        exec_jobs.start_execution()
        res['results'] = exec_jobs.get_results()

        return res


if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) > 0:
        f_in = args[0]
        # Если файла не существует, то выводим ошибку
        if not os.path.isfile(f_in):
            print(f'Invalid filename: {f_in}')
            exit(1)
        out = main(f_in)

        with open('results.json', 'w', encoding='utf-8') as f_out:
            # Запись результатов в 'results.json'
            json.dump(out, f_out, ensure_ascii=False, indent=4)
