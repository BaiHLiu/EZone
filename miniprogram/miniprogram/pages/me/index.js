// pages/me/index.js
const app = getApp()

// let hasLogin = app.globalData.hasLogin
// let userInfo = {
//     "department": wx.getStorageSync('roomdepartment'),
//     "name": wx.getStorageSync('roomname'),
//     "type": wx.getStorageSync('roomtype')
// }


Page({

    /**
     * 页面的初始数据
     */
    data: {
        theme: 'light',
        hasLogin: false,
        userInfo: {},
        roomdepartment: '',
        roomname: '',
        roomtype: '',
        roomnumber: '',
        showTopTips: false,

        radioItems: [
            {name: 'cell standard', value: '0', checked: true},
            {name: 'cell standard', value: '1'}
        ],
        checkboxItems: [
            {name: 'standard is dealt for u.', value: '0', checked: true},
            {name: 'standard is dealicient for u.', value: '1'}
        ],
        items: [
            {name: 'USA', value: '美国'},
            {name: 'CHN', value: '中国', checked: 'true'},
            {name: 'BRA', value: '巴西'},
            {name: 'JPN', value: '日本'},
            {name: 'ENG', value: '英国'},
            {name: 'TUR', value: '法国'},
        ],

        // date: "2016-09-01",
        // time: "12:01",


        departmentlist: [
            '安全与环境工程学院'	,
            '材料科学与工程学院'	,
            '财经学院'	,
            '测绘与空间信息学院'	,
            '地球科学与工程学院'	,
            '电气与自动化工程学院'	,
            '电子信息工程学院'	,
            '公共课教学部'	,
            '海洋科学与工程学院'	,
            '化学与生物工程学院'	,
            '机械电子工程学院'	,
            '计算机科学与工程学院'	,
            '交通学院'	,
            '经济管理学院',
            '能源与矿业工程学院'	,
            '数学与系统科学学院'	,
            '土木工程与建筑学院'	,
            '外国语学院'	,
            '文法学院'	,
            '艺术学院'	,
            '智能装备学院'	,
            '资源学院'	
        ],
        departmentIndex: 0,

        	
        
        isAgree: false,
        formData: {
            "departmentIndex": 0
        },
        rules: [
        {
            name: 'myname',
            rules: {required: true, message: '请输入姓名'},
        }, 
        {
            name: 'mynumber',
            rules: {validator: function(rule, value, param, modeels) {
                if (!value) {
                    return '学号不能为空'
                } else if ( /^\d+$/.test(value) == false ) {
                    return '请输入12位数字学号'
                } else if (value.length !== 12) {
                    return '请输入12位学号'
                }
            }},
        }
    ]
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
        var self = this

        
        //可能的异步bug:，或许settimeout可以解决，使用延长服务器响应时间测试
        self.setData({
            hasLogin: app.globalData.hasLogin
        })
			

        wx.getStorage({ //获取用户本地缓存中的token
            key: 'roomtoken',
            success: (result) => {//成功获取token代表用户已登录或之前登录过

                
                self.setData({
                    hasLogin: true,
                    roomdepartment: wx.getStorageSync('roomdepartment'),
                    roomname: wx.getStorageSync('roomname'),
                    roomtype: wx.getStorageSync('roomtype'),

                    roomnumber: wx.getStorageSync('roomnumber')
                })
            },
            fail: (result) => {//获取token失败代表用户未注册
            }
        })
        // console.log("roomtoken: " + this.data.roomtoken)
        // console.log("roomdepartment: " + this.data.roomdepartment)
        // console.log("roomname: " + this.data.roomname)
        // console.log("roomtype: " + this.data.roomtype)

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
    },

    formInputChange(e) {
        const {field} = e.currentTarget.dataset
        this.setData({
            [`formData.${field}`]: e.detail.value
        })
    },

    bindDepartmentChange: function(e) {

        const field = 'departmentIndex'
        this.setData({
            [`formData.${field}`]: e.detail.value,
            departmentIndex: e.detail.value
        })
        // const tempjson = {"departmentIndex" :e.detail.value}
        // let tempjson = this.data.formData
        // let addjson = {"departmentIndex" :e.detail.value}
        // tempjson.push(addjson)
        // // this.data.formData.push(tempjson)
        // this.setData({
        //     formData: tempjson
        // })

        this.setData({
            countryIndex: e.detail.value
        })
    },
    submitForm() {
        var self = this

        this.selectComponent('#form').validate((valid, errors) => {
            if (!valid) {
                const firstError = Object.keys(errors)
                if (firstError.length) {
                    this.setData({
                        error: errors[firstError[0]].message
                    })

                }
            } else {
                wx.showToast({
                    title: '注册成功！'
                })

                wx.login({//请求微信登录接口
                  success: (res1) => {
                      if (res1.code) {//成功从微信登录接口获取到code
                        // console.log("code:" + res1.code)
                        wx.request({//向后端使用code发送注册请求
                            url: 'https://ezone.catop.top/api/userAPI/register',
                            method: 'POST',
                            header: {
                                "accept": "*/*",
                                "content-type": "application/x-www-form-urlencoded"
                            },
                            dataType: "json",
                            data: {
                                "code" : res1.code,
                                "name" : self.data.formData.myname,
                                "department" : self.data.departmentlist[self.data.formData.departmentIndex],
                                "type" : "public"
                            },
                            success: (res2) => { //注册成功
                                // console.log(res1.code)
                                wx.login({
                                    success: (res4) => {
                                        if (res4.code) {

                                            wx.request({    //请求后端登录接口
                                                url: 'https://ezone.catop.top/api/userAPI/login',
                                                method: 'POST',
                                                header: {
                                                    "accept": "*/*",
                                                    "content-type": "application/x-www-form-urlencoded"
                                                },
                                                dataType: "json",
                                                data: {
                                                    "code": res4.code
                                                },
                                                success: (res3) => {
                                                    
                                                    self.setData({
                                                        hasLogin: true,
                                                        roomdepartment: res3.data.body.department,
                                                        roomname: res3.data.body.name,
                                                        // roomnumber: res3.data.body.number,
                                                        roomnumber: self.data.formData.mynumber,
                                                        roomtype: res3.data.body.type,
                                                        roomtoken: res3.data.body.token
                                                    })
                                                    wx.setStorageSync('roomtoken', res3.data.body.token)//更新token
                                                    wx.setStorageSync('roomdepartment', res3.data.body.department)
                                                    wx.setStorageSync('roomname', res3.data.body.name)
                                                    wx.setStorageSync('roomtype', res3.data.body.type)
                                                    
                                                    wx.setStorageSync('roomnumber', self.data.formData.mynumber)//学号
                                                },
                                                fail: (res3) => {
                                                    
                                                }
                                            })

                                        } else {
                                        }
                                    }
                                })
                                

                                


                            },
                            fail: (res2) => {
                            }
                        })
                      } else {
                    }
                  }
                })
            }
        })
        // this.selectComponent('#form').validateField('mobile', (valid, errors) => {
        //     console.log('valid', valid, errors)
        // })
    },
    /**
     * 生命周期函数--监听页面初次渲染完成
     */
    onReady: function () {

    },

    /**
     * 生命周期函数--监听页面显示
     */
    onShow: function () {

    },

    /**
     * 生命周期函数--监听页面隐藏
     */
    onHide: function () {

    },

    /**
     * 生命周期函数--监听页面卸载
     */
    onUnload: function () {

    },

    /**
     * 页面相关事件处理函数--监听用户下拉动作
     */
    onPullDownRefresh: function () {

    },

    /**
     * 页面上拉触底事件的处理函数
     */
    onReachBottom: function () {

    },

    /**
     * 用户点击右上角分享
     */
    onShareAppMessage: function () {

    }
})