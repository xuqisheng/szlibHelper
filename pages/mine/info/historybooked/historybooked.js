// pages/mine/info/historybooked/historybooked.js
var util = require('../../../../utils/util.js')
var app = getApp()
Page({
  data:{
    start_date: "2015-05-09",
    end_date: "2017-05-09",
    select: 1,
    allow_start_date: "2015-09-01",
    allow_end_date: "2017-09-01",
    list: [
    ],
    pagestate: 0,
  },
  // 响应单选框变化
  checkboxChange: function (e) {
    console.log(e);
    var selected = 0;
    if (e.detail.value.length > 0) {
      var vals = e.detail.value;
      var selected = vals[e.detail.value.length-1];

      var calDates = util.calSelectDateString(selected);
      this.data.start_date = calDates[0];
      this.data.end_date = calDates[1];

      this.setData({
        select: selected,
        start_date: this.data.start_date,
        end_date: this.data.end_date
      })
    }
    console.log("checkbox: " + selected);
  },
  bindDateChange: function(e) {
    console.log(e);
    if (e.currentTarget.dataset.val == 1) {
      this.data.start_date = e.detail.value;
    } else {
      this.data.end_date = e.detail.value;
    }
    this.data.select = 0;
    this.setData({
      select: this.data.select,
      start_date: this.data.start_date,
      end_date: this.data.end_date
    });
  },
  onTapSearch: function(e) {
    this.requestLoanHistory(1);
  },
  requestLoanHistory: function(showSucceedPromot) {
    var that = this;
    var start = util.transDateString(this.data.start_date);
    var end = util.transDateString(this.data.end_date);
    console.log("start: " + this.data.start_date + ", end: " + this.data.end_date);
    console.log("start: " + start + ", end: " + end);
    wx.request({
      url: 'https://www.jiangfuqiang.cn/szlib/getLoanHistory.jsp',
      method: "POST",
      data: {
        username: app.globalData.account,
        password: app.globalData.passwdMd5,
        operation: "getLoanHistory",
        cardno: app.globalData.account,
        startdate: start,
        enddate: end
      },
      header: {
        'content-type': 'application/x-www-form-urlencoded'
      },
      success: function (res) {
        console.log(res);
        that.data.pagestate = 1;
        that.data.list = res.data;
        that.setData({
          list: that.data.list,
          pagestate: 1
        });
        if (showSucceedPromot) {
          wx.showToast({
            title: '查询成功',
            icon: 'success',
            duration: 1000
          });
        }
      },
      fail: function (e) {
        console.log(e);
        that.data.pagestate = 1;
        that.setData({
          pagestate: 1
        });
        wx.showToast({
          title: '查询失败',
          icon: 'success',
          duration: 2000
        });
      }
    })
  },
  onLoad:function(options){
    // 页面初始化 options为页面跳转所带来的参数
    console.log(options);
    console.log("Here: historybooked page");

    var calDates = util.calSelectDateString(1);
    this.data.start_date = calDates[0];
    this.data.end_date = calDates[1];

    this.setData({
      select: 1,
      start_date: this.data.start_date,
      end_date: this.data.end_date
    });
    this.requestLoanHistory(0);
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