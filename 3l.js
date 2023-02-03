var request = require('request-promise');
var md5 = require('md5-node');
var loginOptions = {
    method: 'POST',
    uri: 'http://floor.huluxia.com/account/login/ANDROID/4.0',
    form: {
        "account": process.env.USER,
        "login_type": 2,
        "password": md5(process.env.PSW.toString()),
        "platform": "2",
        "gkey": "000000",
        "app_version": "4.0.0.6.2", // 版本号可能会旧
        "versioncode": "20141433",
        "market_id": "floor_huluxia",
        "device_code": "%5Bw%5D02%3A00%3A00%3A00%3A00%3A00-%5Bi%5D008796755300310",
    },
    headers: {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8", // 设置为 x-www
        "User-Agent": "okhttp/3.8.1",
    },
    json: true
}
var token = "60904488B4506E4DB68B8311D13D505F0AB5D13DB9BF6271BF88512480980A7728D63F86EF275C86E29525D05A75477DBD1B88FACD1536AF";
function signIn() {
    console.log(`=====================${Date()}======================`);
    request('http://floor.huluxia.com/user/status/ANDROID/2.1?_key=' + token).then(resStatus => {
        console.log('当前token:' + token + '  ' + JSON.parse(resStatus).status);
        if (JSON.parse(resStatus).status == 1) {
            console.log('token未过期');
            request('http://floor.huluxia.com/category/list/ANDROID/2.0').then(resC => {
                console.log();
                let categories = JSON.parse(resC).categories;
                // console.log(categories)
                categories.map((v, i, a) => {
                    request({
                        method: 'POST',
                        uri: 'http://floor.huluxia.com/user/signin/ANDROID/4.0',
                        form: {
                            _key: token,
                            cat_id: v.categoryID
                        },
                        headers: {
                            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8", // 设置为 x-www
                            "User-Agent": "okhttp/3.8.1",
                        },
                        json: true
                    }).then(resS => {
                        if (resS.status = 1) {
                            console.log(v.title + '签到成功');
                        } else {
                            console.log(v.title + '签到失败');
                        }
                    })
                })
            })
        } else {
            console.log('token已过期');
            request(loginOptions).then(res => {
                if (res._key) {
                    token = res._key;
                    console.log('新的token:' + token);
                    request('http://floor.huluxia.com/category/list/ANDROID/2.0').then(resC => {
                        console.log();
                        let categories = JSON.parse(resC).categories;
                        // console.log(categories)
                        let allPromose = []
                        categories.map((v, i, a) => {
                            allPromose.push(new Promise((resolve, reject) => {
                                request({
                                    method: 'POST',
                                    uri: 'http://floor.huluxia.com/user/signin/ANDROID/4.0',
                                    form: {
                                        _key: token,
                                        cat_id: v.categoryID
                                    },
                                    headers: {
                                        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8", // 设置为 x-www
                                        "User-Agent": "okhttp/3.8.1",
                                    },
                                    json: true
                                }).then(resS => {
                                    if (resS.status = 1) {
                                        console.log(v.title + '签到成功');
                                        resolve(v.title + '签到成功')
                                    } else {
                                        console.log(v.title + '签到失败!!!!!!!!!!!!!!');
                                        resolve(v.title + '签到失败!!!!!!!!!!!!!!');
                                    }
                                })
                            }))

                        })
                        Promise.all(allPromose).then(res => {
                            // console.log(res);
                            desp = "### 🚀签到\n```";
                            res.map((v, i, a) => {
                                desp += v + '\n'
                            })
                            desp += "```";
                            // console.log(desp);
                            let option = {

                            }
                            request.post(
                                {
                                    method: 'POST',
                                    uri: 'https://sc.ftqq.com/'+process.env.S_KEY+'.send',
                                    form: {
                                        text: '三楼签到',
                                        desp
                                    },
                                    json: true
                                }
                            ).then(res => {
                                console.log(res)
                            });
                        })
                    })
                }
            })
        }
    });
}
signIn();
// setInterval(signIn,86400000);
