from urllib.parse import urlparse
from urllib.parse import quote
from jinja2 import Template
import yaml

# 读取 ymal
with open('blocks.yml', 'r', encoding='utf-8') as f:
    blocks = yaml.load(f.read(), Loader=yaml.FullLoader)

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
    for block in blocks:
        print(gen_block(block))
        for repo in block["repos"]:
            print(gen_repo(repo))

if __name__ == "__main__":
    main()