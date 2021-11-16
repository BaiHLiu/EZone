// app.js
// const util = require('../utils/utils.js')
// Promise封装微信小程序wx.request请求

// 1.定义公共变量,如(url,data等)

const baseUrl = 'https://ezone.catop.top/api';
const moment = require('moment');


const requestHeader = { //header定义的都不一样，你们拉下来后自行修改为你们所用的
	// "content-type": 'application/json',
	// "Authorization": 'Basic ' + base64.encode("7oewtwo8vnh7bq7rd6t4djy9" + ':' + "eq4vxysrhiwbme4ngk0ti1egm3msyvas"),
	// "tenant": 'MDAwMA==',
	// "token": "Bearer " + wx.getStorageSync('token')
}

// 使用promise封装request
const api = {
	requestApi(url, method, data) {
		return new Promise(function (resolve, reject) {
			wx.request({
				url: baseUrl + url,
				method: method,
				data: method === 'POST' ? JSON.stringify(data) : data,
				header: requestHeader,
				success(res) {
					resolve(res) //一定别忘了加成功之后resolve方法
					// 请求成功
					//这里是后端定义的code字段返回规则，你们按各自后端定义的字段规则修改
					if (res.data.err_code == 0) {
						//请求成功
						wx.hideLoading();
					} else if (res.data.err_code == -1) {
						wx.hideLoading();
					} else if (res.data.err_code == -2) {
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


App({
	globalData: {
		openid: null,
		theme: wx.getSystemInfoSync().theme,
		buildings: [],
		roomtoken: '',
		hasLogin: false,
		totalNumberJSON: {},
		roomjson: {},
		userInfo: {
			"department": '',
			"name": '',
			"type": ''
		}
	},
	onLaunch() {
		const self = this
		// console.log("App onLaunch")

		// wx.login({
		// 	success: (res) => {
		// 		console.log(res.code)
		// 	}
		// })

		wx.getStorage({ //获取用户本地缓存中的token
			key: 'roomtoken',
			success: (result) => { //获取成功，代表该微信账号已注册小程序
				// console.log("wx.getStorageSync success" + result)
				wx.login({//直接请求微信登录接口
					success: (res2) => {
						if (res2.code) {
							wx.request({ //向后端使用code发送登录请求
								url: 'https://ezone.catop.top/api/userAPI/login',
								method: 'POST',
								header: {
									"accept": "*/*",
									"content-type": "application/x-www-form-urlencoded"
								},
								dataType: "json",
								data: {
									"code": res2.code
								},
								success: (res3) => {
									if (res3.data.err_code == 0) {//登录成功
										self.globalData.hasLogin = true
										// console.log("self.globalData.hasLogin" + self.globalData.hasLogin)
										wx.setStorageSync('roomtoken', res3.data.body.token)//更新token
										wx.setStorageSync('roomdepartment', res3.data.body.department)
										wx.setStorageSync('roomname', res3.data.body.name)
										wx.setStorageSync('roomtype', res3.data.body.type)

										self.globalData.roomtoken = res3.data.body.token
										self.globalData.userInfo = {
											"department": res3.data.body.department,
											"name": res3.data.body.name,
											"type": res3.data.body.type
										}
									} else if (res3.data.err_code == -1) {//系统错误
									} else if (res3.data.err_code == -2) {//用户未注册
									}
								},
								fail: (res3) => {
								}

							})
						} else {
							
						}
					}
				})
			},
			fail: (result) => { //获取roomtoken失败，需要登录或注册,这里只处理登录,注册写在page/me/index.js
				// console.log("wx.getStorageSync fail" + result)
				wx.login({//请求微信登录接口
					success: (res2) => {
						if (res2.code) {//成功从微信登录接口获取到code
							wx.request({ //向后端使用code发送登录请求
								url: 'https://ezone.catop.top/api/userAPI/login',
								method: 'POST',
								header: {
									"accept": "*/*",
									"content-type": "application/x-www-form-urlencoded"
								},
								dataType: "json",
								data: {
									"code": res2.code
								},
								success: (res3) => {//请求后端成功，还需要判断用户是否注册
									// console.log("请求后端成功，还需要判断用户是否已经注册")
									// console.log(res3.data)
									if (res3.data.err_code == 0) {//登录成功
										self.globalData.hasLogin = true
										wx.setStorageSync('roomtoken', res3.data.body.token)//更新token
										wx.setStorageSync('roomdepartment', res3.data.body.department)
										wx.setStorageSync('roomname', res3.data.body.name)
										wx.setStorageSync('roomtype', res3.data.body.type)

										self.globalData.roomtoken = res3.data.body.token
										self.globalData.userInfo = {
											"department": res3.data.body.department,
											"name": res3.data.body.name,
											"type": res3.data.body.type
										}
									} else if (res3.data.err_code == -1) {//系统错误
									} else if (res3.data.err_code == -2) {//用户未注册,测试注册接口,正式实现在page/me/index.js
									}
								},
								fail: (res3) => {
								}

							})
						} else {
						}
					}
				})
			}
		})
		
		wx.request({//获取可用建筑列表
			url: 'https://ezone.catop.top/api/statisticsAPI/getBuildings',

			success: (res1) => {
				this.globalData.buildings = res1.data.body
				// console.log("app.globalData.buildings:\n" + this.globalData.buildings)
				// if (this.testDataCallback){
				// 	this.testDataCallback(res.data.body);
				// 	console.log(11)
				// }
				wx.request({
					url: 'https://ezone.catop.top/api/statisticsAPI/getBuildingStatus',
					data: {
						"buildingName": res1.data.body[0]
					},

					success: (res2) => {
						let tempjsonS = res2.data;
						for(let key in tempjsonS.body ) {
							if(key.indexOf('null') != -1){
								delete tempjsonS.body[key];
							}
						}

						this.globalData.roomjson = tempjsonS
					}
				})
			}
		})
		wx.request({//预加载统计页面lineCharts表的信息，默认为昨日信息
			url: 'https://ezone.catop.top/api/statisticsAPI/getDailySumData',
			data: {
				"date": moment().subtract(1, 'days').format("YYYY-MM-DD")//获取昨日date字符串
			},
			success: (res) => {
				this.globalData.totalNumberJSON = res.data
				//   console.log(this.globalData.totalNumberJSON)
			}
		})
	},

	watch: function (method, isstr) {
		var obj = this.globalData;
		Object.defineProperty(obj, isstr, {
			configurable: true,
			enumerable: true,
			set: function (value) {
				this._consumerGoodsStatus = value; //_consumerGoodsStatus是Object.defineProperty自定义的属性
				method(value);
			},
			get: function (value) {
				return this._consumerGoodsStatus
			}
		})
	},

	// watch3: function (method, isstr) {
	// 	var obj = this.globalData;
	// 	Object.defineProperty(obj, isstr, {
	// 		configurable: true,
	// 		enumerable: true,
	// 		set: function (value) {
	// 			this._consumerGoodsStatus = value; //_consumerGoodsStatus是Object.defineProperty自定义的属性
	// 			method(value);
	// 		},
	// 		get: function (value) {
	// 			return this._consumerGoodsStatus
	// 		}
	// 	})
	// },
	 // 这里这么写，是要在其他界面监听，而不是在app.js中监听，而且这个监听方法，需要一个回调方法。
	 watch3:function(method, name){
		var obj = this.globalData;
		Object.defineProperty(obj,name, {
		  configurable: true,
		  enumerable: true,
		  set: function (value) {
			this._name = value;
			
			method(value);
		  },
		  get:function(){
		  // 可以在这里打印一些东西，然后在其他界面调用getApp().globalData.name的时候，这里就会执行。
		  
			return this._name
		  }
		})
	  },
	onShow() {



	}


})