// index.js
// 获取应用实例

const app = getApp()
const date = new Date()
const moment = require('moment');
// var setBoxStyle = require('./setBoxStyle.wxs');
const dates = ['今日'] //日期
// var buildings = []//教学楼列表


// const buildings = app.globalData.buildings;
let timeInterval = ['现在']
// const timeInterval =['12节','34节','56节','78节','9X节']//具体时段
const years = moment().format("YYYY") //当前时间的年份
const months = moment().format("M") //当前时间的月份
const days = moment().format("D") //当前时间的日期
const hours = moment().format("k") //当前时间的小时数
const minutes = moment().format("m") //当前时间的分钟数
const seconds = moment().format("s") //当前时间的秒数

let textColor = '#82E0AA'

for (let i = 1; i <= 20; i++) {
	dates.push(moment().add(i, 'days').format("M月D日"))
}



Page({
	data: {
		theme: 'light',
		textColor,
		title: '教室占用情况',
		item_available_style_text: '可用教室',
		item_unavailable_style_text: '已占用教室',

		availableColor: '#339933',
		unavailableColor: '#FFCC33',
		// picker-view-begin
		dates, //日期
		// buildings: ['J1','J3','J5','J7','J14','S1','泰-1','济-1'],//教学楼列表
		buildings: ['S1','J1','J14'],
		isNow: true,
		timeInterval, //具体时段
		tempTimeInterval: [],
		rooms: [],
		value: [0, 0, 0],
		tempvalue: [0, 0, 0],
		progressDuration: 18,
		// testvalue:[0,0,0],
		testtext: '',
		// picker-view-end
		progressStyle: [0.0, 0.0, 0.0, 0.0], //[width, height, top, left]
		/*
		进度条和房间名重叠实现原理：
			在mainPage页面渲染后，会自动调用onLoad()
			在这时使用微信小程序逻辑层提供的SelectorQuery和NodesRef，
			获取页面节点信息（其实就是dom元素信息），
			同时使用这些信息设置wxs暴露出来的propValue,
			propValue被设置后会自动调用渲染层wxs中的propObserver函数，
			此时就可以通过渲染层设置页面节点样式

			又是怀念JQuery的一天（bushi

		*/
		testjson: {
			"body": null,
			"err_code": 0,
			"msg": "ok",
			"prompt": [{
					"available": 0,
					"current_occupy": 12,
					"max_seats": 120,
					"occupy_rate": 0.1,
					"room_name": "J1-201"
				},
				{
					"available": 0,
					"current_occupy": 32,
					"max_seats": 160,
					"occupy_rate": 0.2,
					"room_name": "J1-202"
				},
				{
					"available": 0,
					"current_occupy": 132,
					"max_seats": 160,
					"occupy_rate": 0.83,
					"room_name": "J1-203"
				},
				{
					"available": 1,
					"current_occupy": 62,
					"max_seats": 200,
					"occupy_rate": 0.31,
					"room_name": "J1-204"
				},
				{
					"available": 1,
					"current_occupy": 94,
					"max_seats": 160,
					"occupy_rate": 0.59,
					"room_name": "J1-205"
				},
				{
					"available": 0,
					"current_occupy": 85,
					"max_seats": 120,
					"occupy_rate": 0.71,
					"room_name": "J1-206"
				},
				{
					"available": 1,
					"current_occupy": 99,
					"max_seats": 120,
					"occupy_rate": 0.83,
					"room_name": "J1-207"
				},
				{
					"available": 0,
					"current_occupy": 67,
					"max_seats": 80,
					"occupy_rate": 0.84,
					"room_name": "J1-208"
				},
				{
					"available": 1,
					"current_occupy": 33,
					"max_seats": 120,
					"occupy_rate": 0.28,
					"room_name": "J1-209"
				},
				{
					"available": 0,
					"current_occupy": 57,
					"max_seats": 200,
					"occupy_rate": 0.29,
					"room_name": "J1-210"
				},
				{
					"available": 1,
					"current_occupy": 24,
					"max_seats": 200,
					"occupy_rate": 0.12,
					"room_name": "J1-211"
				},
				{
					"available": 0,
					"current_occupy": 16,
					"max_seats": 160,
					"occupy_rate": 0.1,
					"room_name": "J1-212"
				},
				{
					"available": 1,
					"current_occupy": 130,
					"max_seats": 200,
					"occupy_rate": 0.65,
					"room_name": "J1-213"
				},
				{
					"available": 0,
					"current_occupy": 39,
					"max_seats": 80,
					"occupy_rate": 0.49,
					"room_name": "J1-214"
				},
				{
					"available": 0,
					"current_occupy": 75,
					"max_seats": 160,
					"occupy_rate": 0.47,
					"room_name": "J1-215"
				},
				{
					"available": 0,
					"current_occupy": 40,
					"max_seats": 80,
					"occupy_rate": 0.5,
					"room_name": "J1-216"
				},
				{
					"available": 0,
					"current_occupy": 24,
					"max_seats": 200,
					"occupy_rate": 0.12,
					"room_name": "J1-217"
				},
				{
					"available": 0,
					"current_occupy": 46,
					"max_seats": 200,
					"occupy_rate": 0.23,
					"room_name": "J1-218"
				},
				{
					"available": 0,
					"current_occupy": 16,
					"max_seats": 80,
					"occupy_rate": 0.2,
					"room_name": "J1-219"
				},
				{
					"available": 0,
					"current_occupy": 24,
					"max_seats": 120,
					"occupy_rate": 0.2,
					"room_name": "J1-220"
				},
				{
					"available": 1,
					"current_occupy": 62,
					"max_seats": 120,
					"occupy_rate": 0.52,
					"room_name": "J1-221"
				},
				{
					"available": 1,
					"current_occupy": 103,
					"max_seats": 120,
					"occupy_rate": 0.86,
					"room_name": "J1-222"
				},
				{
					"available": 1,
					"current_occupy": 115,
					"max_seats": 200,
					"occupy_rate": 0.58,
					"room_name": "J1-223"
				},
				{
					"available": 0,
					"current_occupy": 28,
					"max_seats": 120,
					"occupy_rate": 0.24,
					"room_name": "J1-224"
				},
				{
					"available": 1,
					"current_occupy": 15,
					"max_seats": 120,
					"occupy_rate": 0.13,
					"room_name": "J1-225"
				},
				{
					"available": 0,
					"current_occupy": 104,
					"max_seats": 160,
					"occupy_rate": 0.65,
					"room_name": "J1-226"
				},
				{
					"available": 1,
					"current_occupy": 27,
					"max_seats": 80,
					"occupy_rate": 0.34,
					"room_name": "J1-227"
				},
				{
					"available": 0,
					"current_occupy": 51,
					"max_seats": 120,
					"occupy_rate": 0.43,
					"room_name": "J1-228"
				},
				{
					"available": 1,
					"current_occupy": 73,
					"max_seats": 160,
					"occupy_rate": 0.46,
					"room_name": "J1-229"
				},
				{
					"available": 0,
					"current_occupy": 52,
					"max_seats": 160,
					"occupy_rate": 0.33,
					"room_name": "J1-230"
				},
				{
					"available": 1,
					"current_occupy": 90,
					"max_seats": 200,
					"occupy_rate": 0.45,
					"room_name": "J1-231"
				},
				{
					"available": 1,
					"current_occupy": 72,
					"max_seats": 120,
					"occupy_rate": 0.6,
					"room_name": "J1-232"
				},
				{
					"available": 0,
					"current_occupy": 158,
					"max_seats": 200,
					"occupy_rate": 0.79,
					"room_name": "J1-233"
				},
				{
					"available": 1,
					"current_occupy": 76,
					"max_seats": 120,
					"occupy_rate": 0.64,
					"room_name": "J1-234"
				},
				{
					"available": 0,
					"current_occupy": 30,
					"max_seats": 160,
					"occupy_rate": 0.19,
					"room_name": "J1-235"
				},
				{
					"available": 0,
					"current_occupy": 78,
					"max_seats": 200,
					"occupy_rate": 0.39,
					"room_name": "J1-236"
				},
				{
					"available": 1,
					"current_occupy": 27,
					"max_seats": 120,
					"occupy_rate": 0.23,
					"room_name": "J1-237"
				},
				{
					"available": 1,
					"current_occupy": 85,
					"max_seats": 120,
					"occupy_rate": 0.71,
					"room_name": "J1-238"
				},
				{
					"available": 0,
					"current_occupy": 34,
					"max_seats": 80,
					"occupy_rate": 0.43,
					"room_name": "J1-239"
				}
			]
		},
		roomjson: {}
	},

	onLoad() {
		var self = this
		const newMoment = moment().subtract(parseInt(hours), 'hours').subtract(parseInt(minutes), 'minutes').subtract(parseInt(seconds), 'seconds') //将现在的时间中的时分秒清零保存到新对象中


		const completeTimeInterval = ['12节', '34节', '56节', '78节', '9X节']
		let tempTimeInterval = ['现在']
		if (moment().isBefore(newMoment.add(8, 'hours').add(30, 'minutes'))) {
			tempTimeInterval.push('12节', '34节', '56节', '78节', '9X节')	
			// console.log("12")
		} else if (moment().isBefore(newMoment.add(3, 'hours'))) {
			tempTimeInterval.push('34节', '56节', '78节', '9X节')
			// console.log("34")
		} else if (moment().isBefore(newMoment.add(3, 'hours'))) {
			tempTimeInterval.push('56节', '78节', '9X节')
			// console.log("56")
		} else if (moment().isBefore(newMoment.add(2, 'hours'))) {
			tempTimeInterval.push('78节', '9X节')
		} else if (moment().isBefore(newMoment.add(3, 'hours'))) {
			tempTimeInterval.push('9X节')
		}
		setTimeout(() => {
			self.setData({
				timeInterval: tempTimeInterval
			})
		}, 100);

		//可能的bug：第二个滚轮没有数据，即没有拉取到数据
		// app.watch(function (data) {
		// 	// console.log("app.watch function(data):\n" + data)
		// 	self.setData({
		// 		buildings: data,
		// 		testtext: self.data.dates[0] + data[0] + self.data.timeInterval[0]
		// 	})
		// }, "buildings")

		//给roomjson赋初值
		app.watch(function (data) {
			self.setData({
				roomjson: data
			})
			// console.log("app.watch(function (data) {")
			// console.log(data)
			// console.log(data)

			//更新wxml：
			const query = self.createSelectorQuery()

			query.select('.room-text-box').boundingClientRect(function (res) {
				self.setData({
					propValue: [1, res.height]
				})
				// console.log(res)
			})
			query.exec()
		}, "roomjson")

		this.setData({
			theme: wx.getSystemInfoSync().theme || 'light'
		})

		
		if (wx.onThemeChange) {
			wx.onThemeChange(({
				theme
			}) => {
				this.setData({
					theme
				})
			})
		}



		// console.log(app.globalData.progressStyle)



		// setBoxStyle.changeStyle(
		//   app.globalData.progressWidth,
		//   app.globalData.progressHeight,
		//   app.globalData.progressTop,
		//   app.globalData.progressLeft
		// )
		// var instance = ownerInstance.selectComponent('.room-text-box') // 返回组件的实例
		// instance.setStyle({
		//     "width": progressWidth ,
		//     "height": progressHeight

		// })
		// console.log("index onLoad")
	},

	onShow() {
		// console.log("index onShow")
	},


	// 1-2 8:00~9:50
	// 3-4 11:10~12:00
	// 5-6 14：00~15：50
	// 7-8 16：10~18：00
	// 9-X 19：00~20：50
	//picker-begin
	bindChange(event) {
		const val = event.detail.value
		var self = this

		const newMoment = moment().subtract(parseInt(hours), 'hours').subtract(parseInt(minutes), 'minutes').subtract(parseInt(seconds), 'seconds') //将现在的时间中的时分秒清零保存到新对象中
		const completeTimeInterval = ['12节', '34节', '56节', '78节', '9X节']
		let tempTimeInterval = ['现在']
		if (moment().isBefore(newMoment.add(8, 'hours').add(30, 'minutes'))) {
			tempTimeInterval.push('12节', '34节', '56节', '78节', '9X节')	
		} else if (moment().isBefore(newMoment.add(3, 'hours'))) {
			tempTimeInterval.push('34节', '56节', '78节', '9X节')
		} else if (moment().isBefore(newMoment.add(3, 'hours'))) {
			tempTimeInterval.push('56节', '78节', '9X节')
		} else if (moment().isBefore(newMoment.add(2, 'hours'))) {
			tempTimeInterval.push('78节', '9X节')
		} else if (moment().isBefore(newMoment.add(3, 'hours'))) {
			tempTimeInterval.push('9X节')
		}
		
		//把timeInterval滚轮按条件更新
		if(this.data.dates[val[0]] == '今日') {
			self.setData({
				timeInterval: tempTimeInterval
			})
		} else {
			self.setData({
				timeInterval: completeTimeInterval
			})
		}

		//根据时间变化查询方式
		if(this.data.dates[val[0]] == '今日' && this.data.timeInterval[val[2]] == '现在'){//查询实时的教室人数
			wx.request({
				url: 'https://ezone.catop.top/api/statisticsAPI/getBuildingStatus',
				data: {
				  "buildingName": self.data.buildings[val[1]]
				},
	
				success: (res2) => {
				  
				  let tempjsonS = res2.data;
				  for(let key in tempjsonS.body ) {
					  if(key.indexOf('null') != -1){
						  delete tempjsonS.body[key];
					  }
				  }
				  self.setData({
					roomjson: tempjsonS,
					progressDuration: 18
				  })
				//   console.log(tempjsonS)
				  const query = self.createSelectorQuery()
	
					query.select('.room-text-box').boundingClientRect(function (res) {
						self.setData({
							propValue: [1, res.height]
						})
						// console.log(res)
					})
					query.exec()
				  // console.log("success: (res2) => {")
				  // console.log(res2.data)
				}
			  })
		} else if ( this.data.dates[val[0]] == '今日' ) {//查询今天剩余课时下的预约情况
			console.log("this.data.dates[val[0]] == '今日'")
			var requestPeriod = 0
			if( this.data.timeInterval[val[2]] == '12节' ) {
				requestPeriod = 1
			} else if ( this.data.timeInterval[val[2]] == '34节' ) {
				requestPeriod = 3
			} else if ( this.data.timeInterval[val[2]] == '56节' ) {
				requestPeriod = 5
			} else if ( this.data.timeInterval[val[2]] == '78节' ) {
				requestPeriod = 7
			} else if ( this.data.timeInterval[val[2]] == '9X节' ) {
				requestPeriod = 9
			}
			// console.log("requestPeriod: " + requestPeriod)

			wx.request({
				url: 'https://ezone.catop.top/api/statisticsAPI/getBuildingStatus',
				data: {
				  "buildingName": self.data.buildings[val[1]],
				  "date": moment().format("YYYY-MM-DD"),
				  "period": requestPeriod
				},
	
				success: (res2) => {
					let tempjsonS = res2.data;
				  for(let key in tempjsonS.body ) {
					  if(key.indexOf('null') != -1){
						  delete tempjsonS.body[key];
					  }
				  }
				  self.setData({
					roomjson: tempjsonS,
					progressDuration: 10
				  })
				  const query = self.createSelectorQuery()
	
					query.select('.room-text-box').boundingClientRect(function (res) {
						self.setData({
							propValue: [1, res.height]
						})
					})
					query.exec()
				}
			  })


		} else {//查询未来的教室占用情况
			var requestPeriod = 0
			if( this.data.timeInterval[val[2]] == '12节' ) {
				requestPeriod = 1
			} else if ( this.data.timeInterval[val[2]] == '34节' ) {
				requestPeriod = 3
			} else if ( this.data.timeInterval[val[2]] == '56节' ) {
				requestPeriod = 5
			} else if ( this.data.timeInterval[val[2]] == '78节' ) {
				requestPeriod = 7
			} else if ( this.data.timeInterval[val[2]] == '9X节' ) {
				requestPeriod = 9
			}

			wx.request({
				url: 'https://ezone.catop.top/api/statisticsAPI/getBuildingStatus',
				data: {
				  "buildingName": self.data.buildings[val[1]],
				  "date": moment().format("YYYY") + moment(self.data.dates[val[0]], "M月D日").format("-MM-DD"),
				  "period": requestPeriod
				},
	
				success: (res2) => {
					let tempjsonS = res2.data;
					for(let key in tempjsonS.body ) {
						if(key.indexOf('null') != -1){
							delete tempjsonS.body[key];
						}
					}
					self.setData({
						roomjson: tempjsonS,
						progressDuration: 10
					})
				  
				  const query = self.createSelectorQuery()
	
					query.select('.room-text-box').boundingClientRect(function (res) {
						self.setData({
							propValue: [1, res.height]
						})
					})
					query.exec()
				}
			  })
		}
		

		  self.setData({
			testtext: this.data.dates[val[0]] + this.data.buildings[val[1]] + this.data.timeInterval[val[2]],
			propValue: this.data.progressStyle,
		 
			value: val
		})


	} //picker-end

})