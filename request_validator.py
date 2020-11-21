class Validator:
    def __init__(self, data):
        self._data = data
        self._res = {}

    def get_res(self):
        '''
        Возвращает словарь с первой встретившейся ошибкой.
        '''
        return self._res

    def is_valid_data(self):
        '''
        Возвращает True, если ошибок нет.
        '''
        if self._is_valid_size():
            if self._is_valid_jobs():
                return self._is_valid_content()
        return False

    def _is_valid_size(self):
        '''
        Возвращает False, если json пустой или есть поля кроме 'jobs'.
        '''
        if len(self._data.keys()) != 1:
            self._res['results'] = {'overall': 'FAIL'}
            self._res['message'] = 'Incorrect parameters'
            return False
        return True

    def _is_valid_jobs(self):
        '''
        Возвращает False, если нет поля 'jobs' или значение в этом поле не list.
        '''
        if not 'jobs' in self._data:
            self._res['results'] = {'overall': 'FAIL'}
            self._res['message'] = f'Unknown field "{[f for f in self._data.keys()][0]}"'
            return False

        if not isinstance(self._data['jobs'], list):
            self._res['results'] = {'overall': 'FAIL'}
            self._res['message'] = 'Field "jobs" must be a list'
            return False

        return True

    def _is_valid_content(self):
        '''
        Возвращает False, если задачи не содержат всех нужных полей.
        Возвращает False, если значения в полях некорректного типа.
        '''
        keys = ('name', 'commands', 'result_directory')

        for job in self._data['jobs']:
            for key in keys:
                if not key in job:
                    self._res['results'] = {'overall': 'FAIL'}
                    self._res['message'] = f'All jobs must contain "{key}" field'
                    return False

            if not isinstance(job['name'], str):
                self._res['results'] = {'overall': 'FAIL'}
                self._res['message'] = 'Field "name" must be a string'
                return False

            if not isinstance(job['commands'], list):
                self._res['results'] = {'overall': 'FAIL'}
                self._res['message'] = 'Field "commands" must be a list'
                return False

            if not isinstance(job['result_directory'], str):
                self._res['results'] = {'overall': 'FAIL'}
                self._res['message'] = 'Field "result_directory" must be a string'
                return False

            for cmd in job['commands']:
                if not isinstance(cmd, str):
                    self._res['results'] = {'overall': 'FAIL'}
                    self._res['message'] = 'Each command must be a string'
                    return False

        return True
