# coding=utf-8
import logging
import random
import urllib.parse
import urllib.request
import requests
from apig_sdk import signer

def send_verify_code(phone_num, verify_code) :
    # 必填,请参考"开发准备"获取如下数据,替换为实际值
    # url = 'https://smsapi.cn-north-4.myhuaweicloud.com:443/sms/batchSendSms/v1'  # APP接入地址(在控制台"应用管理"页面获取)+接口访问URI
    url = 'https://smsapi.cn-north-4.myhuaweicloud.com:443/sms/batchSendSms/v1'  # APP接入地址(在控制台"应用管理"页面获取)+接口访问URI
    # 认证用的appKey和appSecret硬编码到代码中或者明文存储都有很大的安全风险，建议在配置文件或者环境变量中密文存放，使用时解密，确保安全；
    APP_KEY = "1452N28Y80BiN1BpMRVae3ZSuoXT"  # APP_Key
    APP_SECRET = "3nHZn2zDJwGI1aBBjBW3QHHy2NeS"  # APP_Secret
    # sender = "csms12345678"  # 国内短信签名通道号
    sender = "8822071510613"  # 国内短信签名通道号

    TEMPLATE_ID = "96634d6a411c4f9b94a764233c3459ce"  # 模板ID

    # 条件必填,国内短信关注,当templateId指定的模板类型为通用模板时生效且必填,必须是已审核通过的,与模板类型一致的签名名称

    # signature = "华为云短信测试"  # 签名名称
    signature = "桥茵科技"  # 签名名称

    # 必填,全局号码格式(包含国家码),示例:+86151****6789,多个号码之间用英文逗号分隔
    # receiver = "+86151****6789,+86152****7890"  # 短信接收人号码
    receiver = phone_num  # 短信接收人号码

    # 选填,短信状态报告接收地址,推荐使用域名,为空或者不填表示不接收状态报告
    statusCallBack = "192.168.1.55"

    '''
    选填,使用无变量模板时请赋空值 TEMPLATE_PARAM = '';
    单变量模板示例:模板内容为"您的验证码是${1}"时,TEMPLATE_PARAM可填写为'["369751"]'
    双变量模板示例:模板内容为"您有${1}件快递请到${2}领取"时,TEMPLATE_PARAM可填写为'["3","人民公园正门"]'
    模板中的每个变量都必须赋值，且取值不能为空
    查看更多模板规范和变量规范:产品介绍>短信模板须知和短信变量须知
    '''
    TEMPLATE_PARAM = '[ ' + verify_code + ' ]'  #
    # 模板变量，此处以单变量验证码短信为例，请客户自行生成6位验证码，并定义为字符串类型，以杜绝首位0丢失的问题（例如：002569变成了2569）。)

    formData = urllib.parse.urlencode({
        'from': sender,
        'to': receiver,
        'templateId': TEMPLATE_ID,
        'templateParas': TEMPLATE_PARAM,
        'statusCallback': statusCallBack,
        'signature': signature      #使用中国大陆短信通用模板时,必须填写签名名称
    }).encode('ascii')
    print(formData)

    sig = signer.Signer()
    sig.Key = APP_KEY
    sig.Secret = APP_SECRET

    r = signer.HttpRequest("POST", url)
    r.headers = {"content-type": "application/x-www-form-urlencoded"}
    r.body = formData

    sig.Sign(r)
    # print(r.headers["X-Sdk-Date"])
    # print(r.headers["Authorization"])
    resp = requests.request(r.method, r.scheme + "://" + r.host + r.uri, headers=r.headers, data=r.body, verify=False)
    # print(resp.status_code, resp.reason)
    # print(resp.content)
    logging.info(resp.content)

def gen_verify_code() :
    code = random.randint(100000, 999999)
    return str(code)

"""
if __name__ == '__main__':
    send_verify_code('13701742571', '123456')
"""
