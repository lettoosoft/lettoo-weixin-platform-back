# -*- coding:utf-8 -*-
from django.conf import settings
import os
import json
import urllib
import urllib2
import cookielib
import hashlib
import zlib

from pyquery import PyQuery as pq

import re


class WeixinException(Exception):
    def __init__(self, err_msg, ret):
        self.err_msg = err_msg
        self.ret = ret


class Weixin(object):
    def __init__(self,
                 username,
                 password,
                 cookie_filename='cookie.cookie',
                 base_url='https://mp.weixin.qq.com',
                 login_auth_url='https://mp.weixin.qq.com/cgi-bin/login?lang=zh_CN'):
        self.cookiejar = cookielib.MozillaCookieJar(cookie_filename)
        self.opener = urllib2.build_opener(
            urllib2.HTTPRedirectHandler(),
            urllib2.HTTPHandler(debuglevel=0),
            urllib2.HTTPSHandler(debuglevel=0),
            urllib2.HTTPCookieProcessor(self.cookiejar)
        )

        # Identify who we are
        self.opener.addheaders = [
            ('Accept', 'application/json, text/javascript, */*; q=0.01'),
            ('Accept-Encoding', 'gzip,deflate,sdch'),
            ('Accept-Language', 'zh-CN,zh;q=0.8,ar;q=0.6,en;q=0.4'),
            ('Connection', 'keep-alive'),
            # ('Content-Length', '81'),
            ('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8'),
            ('Host', 'mp.weixin.qq.com'),
            ('Origin', 'https://mp.weixin.qq.com'),
            ('Referer', 'https://mp.weixin.qq.com/'),
            ('User-Agent',
             'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'),
            ('X-Requested-With', 'XMLHttpRequest'),
        ]

        self.base_url = base_url
        self.login_auth_url = login_auth_url

        self.username = username
        self.password = password

    def login(self):
        pwd = hashlib.md5(self.password).hexdigest()
        param = {'username': self.username, 'pwd': pwd, 'imgcode': '', 'f': 'json'}
        login_params = urllib.urlencode(param)
        logged_in_page = self.opener.open(self.login_auth_url, login_params)
        data = json.loads(logged_in_page.read())
        '''
        {u'base_resp': {u'err_msg': u'ok', u'ret': 0}, u'redirect_url': u'/cgi-bin/home?t=home/index&lang=zh_CN&token=1819360945'}
        {u'base_resp': {u'err_msg': u'acct/password error', u'ret': -23}}
        '''
        base_resp = data['base_resp']
        err_msg = base_resp['err_msg']
        ret = base_resp['ret']

        if err_msg == u'ok' and ret == 0:
            redirect_url = data['redirect_url']
            self.token = redirect_url.split('&token=')[1]
            return True
        else:
            raise WeixinException(err_msg=err_msg, ret=ret)

    def get_user_info(self):
        url = 'https://mp.weixin.qq.com/cgi-bin/settingpage?t=setting/index&action=index&token=%s&lang=zh_CN' % self.token
        repo = self.opener.open(url)
        html = repo.read()
        if repo.headers.get('Content-Encoding', '') == 'deflate':
            decompress = zlib.decompressobj(
                -zlib.MAX_WBITS
            )
            html = decompress.decompress(html)
            html += decompress.flush()
        d = pq(html)
        account_settings = d.find('li.account_setting_item')
        dict = {}
        for item in account_settings:
            account_setting_item = pq(item)
            h4 = account_setting_item.find('h4')
            name = h4.html().strip()
            value = account_setting_item.find('div.meta_content').html().strip()
            key = name
            if name == u'名称':
                key = 'title'
            elif name == u'微信号':
                key = 'weixin_id'
                value = pq(value).html().strip()
            elif name == u'头像':
                key = 'thumbnail_url'
                value = self.base_url + pq(value).attr('src')
            elif name == u'二维码':
                value = self.base_url + pq(value).attr('href').split("&action=download")[0]
                #open('b.jpg', 'wb').write(self.opener.open(value).read())
            elif name == u'原始ID':
                value = pq(value).html().strip()
            elif name == u'类型':
                key = 'type'
                if value == u'订阅号':
                    value = 'subscribe'
                else:
                    value = 'service'
            else:
                pass

            dict[key] = value

        open('%s/%s.jpg' % (settings.MEDIA_ROOT, dict['weixin_id']), 'wb').write(self.opener.open(dict['thumbnail_url']).read())
        dict['thumbnail_url'] = '/media/%s.jpg' % dict['weixin_id']
        return dict

    def set_url_token(self, url, callback_token):
        url = 'https://mp.weixin.qq.com/advanced/advanced?action=interface&t=advanced/interface&token=%s&lang=zh_CN' % self.token
        repo = self.opener.open(url)
        html = repo.read()
        if repo.headers.get('Content-Encoding', '') == 'deflate':
            decompress = zlib.decompressobj(
                -zlib.MAX_WBITS
            )
            html = decompress.decompress(html)
            html += decompress.flush()
        pattern = 'operation_seq:(.*?)"(.+?)"'
        operation_seq = re.findall(pattern, html)[0][1]

        url = 'https://mp.weixin.qq.com/advanced/callbackprofile?t=ajax-response&token=%s&lang=zh_CN' % self.token
        param = urllib.urlencode(
            {
                'url': url,
                'callback_token': callback_token,
                'operation_seq': operation_seq}
        )
        a = self.opener.open(url, param)
