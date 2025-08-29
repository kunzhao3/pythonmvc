from flask import render_template, redirect


class Html:
    @classmethod
    def render(cls, name, *args, **kwargs):
        return render_template(name, *args, **kwargs)

    @classmethod
    def redirect(cls, url):
        return redirect(url)