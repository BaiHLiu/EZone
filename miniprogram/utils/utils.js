// Promise封装微信小程序wx.request请求

// 1.定义公共变量,如(url,data等)

const baseUrl = 'https://ezone.catop.top/api';

const requestHeader = { //header定义的都不一样，你们拉下来后自行修改为你们所用的
	// "content-type": 'application/json',
	// "Authorization": 'Basic ' + base64.encode("7oewtwo8vnh7bq7rd6t4djy9" + ':' + "eq4vxysrhiwbme4ngk0ti1egm3msyvas"),
	// "tenant": 'MDAwMA==',
	// "token": "Bearer " + wx.getStorageSync('token')
}

// 使用promise封装request
const api = {
	requestApi(url, method, data) {
		return new Promise(function(resolve, reject) {
			wx.request({
				url: baseUrl + url,
				method: method,
				data: method === 'POST' ? JSON.stringify(data) : data,
				header: requestHeader,
				success(res) {
					resolve(res) //一定别忘了加成功之后resolve方法
					// 请求成功
					//这里是后端定义的code字段返回规则，你们按各自后端定义的字段规则修改
					if (res.data.code == 0) {
						//请求成功
						wx.hideLoading();
					} else if (res.data.code == -1) {
                        console.log('内部错误')
						wx.hideLoading();
					} else if (res.data.code == -2) {
                        console.log('当前用户已注册')
						wx.hideLoading();
					} else {
						wx.hideLoading();
						wx.showToast({
							title: res.data.msg,
							icon: 'none',
							duration: 2000
						})
					}
				},
				fail(res) {
					reject(res) //失败之后reject方法
					wx.hideLoading()
					wx.showToast({
						title: '操作失败',
						icon: 'none',
						duration: 2000
					})
				}
			})
		})
	}
}

//导出我们封装好的方法
module.exports.api = api