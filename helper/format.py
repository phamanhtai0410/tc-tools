from datetime import datetime

MONTHS = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12
}


class FormatHelpers:

    @classmethod
    def str_to_num(cls, str_num: str):
        if str_num.isnumeric():
            return int(str_num)
        
        if ',' in str_num:
            return int(str_num.replace(',', ''))

        if 'K' in str_num:
            _num_path = str_num.split('K')[0]
            if '.' in _num_path:
                _k_path = _num_path.split('.')[0]
                _unit_path = _num_path.split('.')[1]
                return int(_k_path) * 1000 + int(_unit_path) * 100
            return int(_num_path) * 1000
        if 'M' in str_num:
            _num_path = str_num.split('M')[0]
            if '.' in _num_path:
                _m_path = _num_path.split('.')[0]
                _unit_path = _num_path.split('.')[1]
                return int(_m_path) * 1000000 + int(_unit_path) * 100000
            return int(_num_path) * 1000000
        if 'B' in str_num:
            _num_path = str_num.split('B')[0]
            if '.' in _num_path:
                _b_path = _num_path.split('.')[0]
                _unit_path = _num_path.split('.')[1]
                return int(_b_path) * 1000000000 + int(_unit_path) * 100000000
            return int(_num_path) * 1000000000

        return 0

    @classmethod
    def str_to_date(cls, str_date: str):
        if not str_date:
            return None
        _month = str_date.split()[0]
        _year = str_date.split()[1]
        _date = datetime(year=int(_year), month=MONTHS[_month], day=1)
        _time = _date.timestamp()
        return {
            'date': _date,
            'time': int(_time)
        }
