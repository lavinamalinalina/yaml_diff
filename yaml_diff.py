import yaml
import difflib



# функция чтения yaml и преобразования в словарь python
def read_yaml(file_path):
    with open(file_path, 'r') as file:
        return list(yaml.load_all(file, yaml.SafeLoader))



# функция преобразования словаря в yaml
def strings_to_yaml(yaml_data):
    return yaml.dump(yaml_data, sort_keys=False, default_flow_style=False, allow_unicode=True)


# функция сравнения и  генерации html
def generate_diff_html(yaml_str1, yaml_str2):
    diff = difflib.HtmlDiff().make_file(
        yaml_str1.splitlines(),
        yaml_str2.splitlines(),
        fromdesc='backup.yaml',
        todesc='dry_run.yaml'
    )

    css = """
    <style type="text/css">
    @media (prefers-color-scheme: dark) {
    html {color: black; text-shadow: 1px 1px 1px black; letter-spacing: 1px;}
    
        body {
            background-color: #1B1B1B;
            color: #E7E8EB;
        }
        a {
            color: #3387CC;    
        }
    }
    @media (prefers-color-scheme: light) {
    html {color: black; text-shadow: 1px 1px 1px black; letter-spacing: 1px;}
    
        body {
        background-color: #1B1B1B;
        color: #E7E8EB;
        }
        a {
            color: #3387CC;
        }
    }
    
        .diff_next {background-color:#dddddd !important; mix-blend-mode: difference;} 
        .diff_add {background-color: #75a15e !important; mix-blend-mode: difference;} 
        .diff_chg {background-color:#ffa943 !important; mix-blend-mode: difference;} 
        .diff_sub {background-color:#b60008 !important; mix-blend-mode: difference;}
        
    #difflib_chg_to@__top {
    width: 100%;
    border-collapse: collapse;
    }
    td:nth-child(3) {
    word-wrap: break-word;
    word-break: break-all;
    white-space: normal;
    width: 47%;
    }
    td:nth-child(6) {
    word-wrap: break-word;
    word-break: break-all;
    white-space: normal;
    width: 47%;
    }
    }
    td:nth-child(2){
    white-space: nowrap;
    }
    td:nth-child(5){
    white-space: nowrap;
    }
    </style>
    """
    start_index = diff.find('<style type="text/css">')
    end_index = diff.find('</style>', start_index) + len('</style>')
    diff_with_css = diff[:start_index] + css + diff[end_index:]

    return diff_with_css


# эта функция преобразует строки с запятыми в массивы с переносом строки для удобства чтения

def transform_strings_to_lists(data):
    if isinstance(data, dict):
        return {k: transform_strings_to_lists(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [transform_strings_to_lists (element) for element in data]
    elif isinstance(data, str) and ',' in data:
        return [item.strip() for item in data.split(',')]
    else:
        return data



# эта функция удаляет лишние куски и исключает xml из сериализации
def filter_dryrun(file_path):
    with open(file_path, 'r') as file:
        dryrun = file.read()
        manifest_starts = dryrun.find("MANIFEST")
        dryrun = dryrun [manifest_starts + 13::]
        dryrun = dryrun.replace(": |-", ":")
        dryrun = dryrun.replace(": |", ":")
        dryrun = dryrun.replace(".xml:", ".xml: |")

    with open(file_path, 'w') as file:
        file.write(dryrun)

# аналогично filter_dryrun
def filter_backup (file_path):
    with open(file_path, 'r') as file:
        backup = file.read()
        backup = backup.replace(": |-", ":")
        backup = backup.replace(": |", ":")
        backup = backup.replace(".xml:", ".xml: |")
    with open(file_path, 'w') as file:
        file.write(backup)


def main(file1, file2):
    filter_backup(file1)
    filter_dryrun(file2)

    yaml1 = read_yaml(file1)
    yaml2 = read_yaml(file2)

    yaml1 = transform_strings_to_lists(yaml1)
    yaml2 = transform_strings_to_lists(yaml2)

    yaml_str1 = strings_to_yaml(yaml1)
    yaml_str2 = strings_to_yaml(yaml2)

    html_diff = generate_diff_html(yaml_str1, yaml_str2)
    with open('report.html', 'w') as report_file:
        report_file.write(html_diff)

if __name__ == '__main__':
    file1 = 'backup.yaml'
    file2 = 'dry_run.yaml'
    main(file1, file2)
