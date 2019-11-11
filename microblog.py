# 作者：hao.ren3
# 时间：2019/11/5 14:34
# IDE：PyCharm

from app import create_app, db
from app.model import User, Post

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}

@app.template_filter('md')
def markdown_html(txt):
    from markdown import markdown
    # return markdown(txt, extensions=[
    #                                   'markdown.extensions.extra',
    #     'markdown.extensions.abbr', 'markdown.extensions.attr_list',
    #     'markdown.extensions.def_list', 'markdown.extensions.tables',
    #     'markdown.extensions.fenced_code', 'markdown.extensions.footnotes',
    #     'markdown.extensions.smart_strong', 'markdown.extensions.admonition',
    #     'markdown.extensions.codehilite', 'markdown.extensions.headerid',
    #     'markdown.extensions.meta', 'markdown.extensions.nl2br',
    #     'markdown.extensions.sane_lists', 'markdown.extensions.smarty',
    #     'markdown.extensions.toc', 'markdown.extensions.wikilinks'
    #                               ])
    return markdown(txt, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.admonition',
        'markdown.extensions.codehilite',
        'markdown.extensions.meta',
        'markdown.extensions.nl2br',
        'markdown.extensions.sane_lists',
        'markdown.extensions.smarty',
        'markdown.extensions.toc',
        'markdown.extensions.wikilinks'
    ])
