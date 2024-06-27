import yaml
import difflib


#функция чтения ямл
def read_yaml(file_path):
    with open(file_path, 'r') as file:
       # print(list(yaml.load_all(file, yaml.SafeLoader)))
        return list(yaml.load_all(file, yaml.SafeLoader))



#функция преобразования ямл в стринг
def yaml_to_string(yaml_data):
    return yaml.dump(yaml_data, sort_keys=False)

#функция сравнения и  генерации html
def generate_diff_html(yaml_str1, yaml_str2):
    diff = difflib.HtmlDiff().make_file(
        yaml_str1.splitlines(),
        yaml_str2.splitlines(),
        fromdesc='file1.yaml',
        todesc='file2.yaml'
    )
    return diff

def main(file1, file2):
    yaml1 = read_yaml(file1)
    yaml2 = read_yaml(file2)

    yaml_str1 = yaml_to_string(yaml1)
    yaml_str2 = yaml_to_string(yaml2)

    html_diff = generate_diff_html(yaml_str1, yaml_str2)

    with open('report.html', 'w') as report_file:
        report_file.write(html_diff)


if __name__ == '__main__':
    file1 = 'file1.yaml'
    file2 = 'file2.yaml'
    main(file1, file2)
