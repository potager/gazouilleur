#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re, time
from hashlib import sha512
from w3lib.html import replace_entities
from gazouilleur.lib.templater import Templater

# TODO:
# - handle error pages
# - handle redirects
# - store screenshot via manet

class WebMonitor(Templater):

    def __init__(self, name, url):
        Templater.__init__(self)
        self.name = name
        self.url = url
        basedir = os.path.join('web', 'monitor')
        self.path = os.path.join(basedir, name)
        if not os.path.exists(basedir):
            os.makedirs(basedir)
            os.chmod(basedir, 0o755)
        if not os.path.exists(self.path):
            os.makedirs(self.path)
            os.chmod(self.path, 0o755)
        self.versions = self.get_versions()

    def get_versions(self):
        files = os.listdir(os.path.join('web', 'monitor', self.name))
        versions = [f.replace(".html", "") for f in files if f.endswith(".html")]
        return sorted(versions)

    def get_last(self):
        if self.versions:
            return self.versions[-1]
        return None

    def get_file(self, version, ftype):
        return os.path.join(self.path, "%s.%s" % (version, ftype))

    def add_version(self, data):
        version = time.strftime("%y%m%d-%H%M")
        for ftype in data:
            name = self.get_file(version, ftype)
            with open(name, "w") as f:
                f.write(data[ftype])
            os.chmod(name, 0o644)
        self.versions.append(version)

    def check_new(self, page):
        page = decode_page(page)
        html = absolutize_links(self.url, page)
        new = {
            "html": html.encode('utf-8'),
            "links": u"\n".join(extract_links(html)).encode('utf-8'),
            "txt": extract_raw_text(page).encode('utf-8')
        }
        last = self.get_last()
        if not last:
            self.add_version(new)
            return
        with open(self.get_file(last, "links")) as f:
            lastlinks = f.read()
        with open(self.get_file(last, "txt")) as f:
            lasttext = f.read()
        if differ(lastlinks, new["links"]) or differ(lasttext, new["txt"]):
            self.add_version(new)
            msg = u"Looks like the monitored page %s at %s just changed!" % (self.name, self.url)
            if self.public_url:
                self.build_diff_page()
                msg += u"\nYou can check the different versions and diffs at %smonitor_%s.html" % (self.public_url, self.name)
            return msg.encode("utf-8")

    def build_diff_page(self):
        data = {
          "name": self.name,
          "url": self.url,
        }
        data["versions"] = sorted(self.versions, reverse=True)
        self.render_template("monitor.html", self.name, data)


# Diff long strings
sha = lambda text: sha512(text).digest()
differ = lambda old, new: len(old) != len(new) or sha(old) != sha(new)


# Get html string data as unicode
def decode_page(data):
    if isinstance(data, unicode):
        return data
    for encoding in ['utf-8', 'latin-1', 'iso-8859-15', 'cp1252', 'unicode-escape']:
        try:
            return unicode(data, encoding)
        except: pass
    return data

# Make all links absolute by rewriting domain and path when needed
re_abslink = re.compile(ur'(src|href)="((https?:)?//)', re.I)
re_rootlink = re.compile(ur'(src|href)="/', re.I)
re_rellink = re.compile(ur'(src|href)="', re.I)
re_host = re.compile(ur'^(https?://[^/]+)/?.*$', re.I)
re_folder = re.compile(ur'^(.*?)(/[^/]*)?$', re.I)
re_css = re.compile(ur'<link (?:[^>]*(?:rel="stylesheet"|type="text/css") [^>]*href="[^"]+"|href="[^"]+"[^>]* (?:rel="stylesheet"|type="text/css"))[^>]*>', re.I)
re_link = re.compile(ur'<(?:a|img|script) [^>]*(?:src|href)="[^"]+"[^>]*>', re.I)
def _absolutize_link(link, host, folder):
    if re_abslink.search(link):
        return link
    if re_rootlink.search(link):
        return re_rootlink.sub(ur'\1="' + host + u'/', link)
    return re_rellink.sub(ur'\1="' + folder + u'/', link)
def absolutize_links(url, html):
    html2 = html
    host = re_host.sub(ur'\1', url)
    folder = re_folder.sub(ur'\1', url)
    for regexp in re_css, re_link:
        for link in regexp.findall(html):
            html2 = html2.replace(link, _absolutize_link(link, host, folder))
    return html2


# Remove everything but actual text from an html document
re_clean_comments = re.compile(ur'<!--.*?-->', re.I|re.DOTALL)
re_clean_javascript = re.compile(ur'<script[^>]*/?>.*?</script>', re.I|re.DOTALL)
re_clean_style = re.compile(ur'<style[^>]*/?>.*?</style>', re.I|re.DOTALL)
re_clean_balises = re.compile(ur'<[/!?]?\[?[a-z0-9\-]+[^>]*>', re.I|re.DOTALL)
re_clean_blanks = re.compile(ur'[ \t\f\v]+')
re_clean_multiCR = re.compile(ur'( ?[\n\r]+)+',re.M)
def extract_raw_text(html):
    text = replace_entities(html)
    text = re_clean_blanks.sub(u' ', text)
    text = re_clean_comments.sub(u' ', text)
    text = re_clean_javascript.sub(u' ', text)
    text = re_clean_style.sub(u' ', text)
    text = re_clean_balises.sub(u' ', text)
    text = re_clean_blanks.sub(u' ', text).strip()
    text = re_clean_multiCR.sub(u'\n\r', text)
    return text


# Extract all links from an html document
re_links = re.compile(r"<a[^>]*href\s*=\s*(\"[^\">]+[\">]|'[^'>]+['>]|[^\s>]+[\s>])", re.DOTALL | re.I)
def extract_links(html):
    return [l.strip(u"\t\r\n '\">") for l in re_links.findall(html)]
