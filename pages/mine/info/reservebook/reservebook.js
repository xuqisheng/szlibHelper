// pages/mine/info/reservebook/reservebook.js
var util = require('../../../../utils/util.js')
var app = getApp()
Page({
  data:{
    list: [
    ]
  },
  onLoad:function(options){
    // 页面初始化 options为页面跳转所带来的参数
    console.log(options);
    console.log("Here: reservebook page");
    var that = this;
    wx.request({
      url: 'https://www.jiangfuqiang.cn/szlib/getReserveBook.jsp',
      method: "POST",
      data: {
        username: app.globalData.account,
        password: app.globalData.passwdMd5,
        operation: "getReserveBook",
        reader: app.globalData.account
      },
      header: {
        'content-type': 'application/x-www-form-urlencoded'
      },
      success: function (res) {
        console.log(res);
        console.log("reserve book: " + res.data.record);
        console.log(res.data.record[0])
        that.data.list = res.data.record;
        console.log("the list: " + that.data.list);
        that.setData({
          list: that.data.list
        })
      },
      fail: function (e) {
        console.log(e);
      }
    })
  },
  onReady:function(){
    // 页面渲染完成
  },
  onShow:function(){
    // 页面显示
    console.log("what the reserver fuck");
  },
  onHide:function(){
    // 页面隐藏
  },
  onUnload:function(){
    // 页面关闭
  }
})