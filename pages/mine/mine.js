// pages/mine/mine.js
var util = require('../../utils/util.js')
var app = getApp()
Page({
  data:{
    list: [
      {
        id: 'historbooked',
        name: '历史借阅',
        open: false,
        page: 'info/historybooked/historybooked'
      }, {
        id: 'reservebook',
        name: '我的预借',
        open: false,
        page: 'info/reservebook/reservebook'
      },
      {
        id: 'finance',
        name: '我的财经',
        open: false,
        page: '../info/generalInfo'
      }, {
        id: 'libary_info',
        name: '我的读者证',
        open: false,
        page: '../info/generalInfo'
      }, {
      /*
        id: 'person_info',
        name: '个人信息',
        open: false
      }, {
      */
        id: 'logout',
        name: '退出登录',
        page: '../login/login',
        open: false
      }
    ]
  },
  kindTapMineItem: function (e) {
    console.log(e);
    var index = e.currentTarget.dataset.index;
    var id = this.data.list[index].id;
    var page = this.data.list[index].page
    console.log("index: " + index + ", id: " + id);
    if (id=='logout') {
      wx.redirectTo({
        url: page,
      });
    } else if (id == 'finance' || id == 'libary_info') {
      if (util.isEmptyObject(app.readerData)) {
        wx.showToast({
          title: '拉取信息失败',
          icon: 'success',
          duration: 2000
        });
      } else {
        wx.navigateTo({
          url: "info/generalInfo?page=" + id,
          fail: function (res) {
            // fail
          },
        });
      }
    } else {
      console.log("be going to: " + page);
      wx.navigateTo({
        url: page,
        fail: function (res) {
          // fail
        },
      });
    }
  },
  onLoad:function(options){
    // 页面初始化 options为页面跳转所带来的参数
    wx.setNavigationBarTitle({
      title: '深图小助手'
    })
    // get reader info
    wx.request({
      url: 'https://www.jiangfuqiang.cn/szlib/getReaderInfo.jsp',
      method: 'POST',
      data: {
        username: app.globalData.account,
        password: app.globalData.passwdMd5,
        operation: "getReaderInfo",
        cardno: app.globalData.account
      },
      header: {
          'content-type': 'application/x-www-form-urlencoded'
      },
      success: function(res){
        // success
        console.log(res.data);
        app.readerData = res.data;
      },
      fail: function(res) {
        // fail
        console.log(res);
        app.readerData = {};
      }
    })
  },
  onReady:function(){
    // 页面渲染完成
  },
  onShow:function(){
    // 页面显示
  },
  onHide:function(){
    // 页面隐藏
  },
  onUnload:function(){
    // 页面关闭
  }
})
