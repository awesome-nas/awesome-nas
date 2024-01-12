from urllib.parse import urlparse
from urllib.parse import quote
from jinja2 import Template
import yaml

def genReadme(replacement_text):
    # 读取 README.md 文件内容
    with open('../README.md', 'r') as file:
        content = file.read()

    # 定义要替换的文本
    start_marker = '<!-- autogen start -->'
    end_marker = '<!-- autogen end -->'

    # 在文件内容中找到并替换标记之间的文本
    start_index = content.find(start_marker)
    end_index = content.find(end_marker) + len(end_marker)
    new_content = content[:start_index] + start_marker + '\n' + replacement_text + end_marker + content[end_index:]

    # 将修改后的内容写回文件
    with open('../README.md', 'w') as file:
        file.write(new_content)

# 使用配置文件生成内容
def genFromProjectsYml():

    # 读取 ymal
    with open('projects.yml', 'r', encoding='utf-8') as f:
        blocks = yaml.load(f.read(), Loader=yaml.FullLoader)

    genContent = ""

    for block in blocks:
        genContent += gen_block(block)+"\n"
        for repo in block["repos"]:
            genContent += gen_repo(repo) +"\n"

    return genContent


# shields 服务基础地址
shields_base_url = "https://img.shields.io/github"

# 块模板
block_tmpl = """
## {{block_name}}
_{{block_desc}}_

| 🔗      | Last Version | Last Commit | Last Releases | License | Stars | Top language |
| :------ | :------ | :------ | :------ | :------ | :------ | :------ |
"""

# 仓库模板
repo_tmpl = """|[{{repo_name}}](https://github.com/{{user}}/{{repo}})|![图]({{shields_base_url}}/v/release/{{user}}/{{repo}}?label= "title")|![图]({{shields_base_url}}/last-commit/{{user}}/{{repo}}?label= "title")|![图]({{shields_base_url}}/release-date/{{user}}/{{repo}}?label= "title")|![图]({{shields_base_url}}/license/{{user}}/{{repo}}?label= "title")|![图]({{shields_base_url}}/stars/{{user}}/{{repo}}?label=&style=flat "title")|![图]({{shields_base_url}}/languages/top/{{user}}/{{repo}} "title")|"""

def gen_block(block):
    return Template(block_tmpl).render(block_name=block["name"],block_desc=block["desc"])

def gen_repo(repo):
    path_parts = urlparse(repo["url"]).path.split("/")
    return Template(repo_tmpl).render(shields_base_url=shields_base_url, repo_name=repo["name"], user=path_parts[1], repo=path_parts[2])

def main():
    genReadme(genFromProjectsYml())

if __name__ == "__main__":
    main()