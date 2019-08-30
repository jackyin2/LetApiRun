# LetApiRun

首先跟大家介绍下letapirun的参考样本，一个是感谢大神九毫（debugtalk）一个是感谢unittest框架， 
感谢debugtalk是因为他让我知道了如何更加方便的用例管理方式json/yaml，感谢unittest是因为借鉴了unittest的用例编写方式，通过将用例json文档化，
来实现LetApiRun

{
   "test": [{
     "name": "login_commuity_with_jack",

     "setupcase": {
       "success": "${__get_value('success')}",
       "abc":123,
       "c":3,
       "fun2":"${__get_value(a=1, b=2)}",
       "username": "jack"
     },

     "requestor":{
        "url": "${host}/telwoy/device-mgr/api/auth/login",
        "method": "POST",
        "headers": {
          "content-type": "application/json"
       },
     "data": { "username": "${username}", "password": "111111"}
     },

     "validator": {
       "status_code": 200,
       "headers": {"Content-Type": "application/json;charset=UTF-8"},
       "assertEqStr": ["100000"],
       "assertEqJson":{"success":true}
     },

     "collector":{
       "json": {"token": "response.data.token"},
       "methods": {
         "cookie":"${__collect_value(re, 'headers', 'cookie')}"
       }
     },

     "teardowncase":{
       "clear_cookies": "clearcookies",
       "clearsession": "clearsession",
       "cleartoken": "cleartoken"
     }
   }]
}
