// pages/mine/info/reservebook/reservebook.js
var util = require('../../../../utils/util.js')
var app = getApp()
Page({
  data:{
    list: [
    ],
    pagestate: 0,
  },
  onCoverLoadError: function (e) {
    console.log(e);
    console.log("What's going on!!!");

    var index = e.target.dataset.index;
  
    // update img state
    this.data.list[index]["imgstate"] = 2;
    var keyStr = "list[" + index + "].imgstate"
    var valDict = {};
    valDict[keyStr] = "2";
    this.setData(valDict);
  
    // reset img source
    var _errImg = e.target.dataset.errImg;
    var _errObj = {};
    //_errObj[_errImg]="../../loan_book.png";
    _errObj[_errImg] = "https://www.jiangfuqiang.cn/getSzlibCover/" + this.data.list[index].isbn + ".jpg";
    this.data.list[index].img;
    console.log("reset img as: " + _errObj[_errImg]);

    //console.log( e.detail.errMsg+"----"+ _errObj[_errImg] + "----" +_errImg ); 
    this.setData(_errObj);
  },
  onTapReloadCover: function (e) {
    var index = e.target.dataset.index;
    console.log("tap cover: " + index);
    console.log(e);
    console.log(this.data.list);
    if (this.data.list[index].imgstate == 2) {
      // reset img
      var _errImg = "list[" + index + "].img";
      var _errObj = {};
      _errObj[_errImg] = this.data.list[index].img;
      //_errObj[_errImg] = "../../loan_book.png";
      console.log("reset img as: " + _errObj[_errImg]);
      console.log("----" + _errObj[_errImg] + "----" + _errImg);
      this.setData(_errObj);
    }
  },
  onLoad:function(options){
    // 页面初始化 options为页面跳转所带来的参数
    console.log(options);
    console.log("Here: reservebook page");
    wx.setNavigationBarTitle({
      title: '我的预借'
    })
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
        that.data.pagestate = 1;
        that.setData({
          pagestate: 1
        });
        if (res.statusCode == 200) {
          that.data.list = res.data.record;
          for (var index=0; index<that.data.list.length;index++) {
            var isbn = that.data.list[index].isbn;
            if (index > 0) {
              (function(myIndex, myIsbn) {
                setTimeout(function() {
                  var key = "list[" + myIndex + "].img";
                  var coverUrl = "http://202.112.150.126/index.php?client=szlib&isbn=" + myIsbn +"/cover";
                  var currentTime = new Date();
                  console.log("currentTime: " + currentTime);
                  console.log(key + " : " + coverUrl);
                  var _errObj={};
                  _errObj[key]= coverUrl;
                  that.setData(_errObj);
                }, 200*index);
              })(index, isbn);
              that.data.list[index]["img"] = "";
            } else {
              that.data.list[index]["img"] = "http://202.112.150.126/index.php?client=szlib&isbn="+ isbn +"/cover";
            }
            that.data.list[index]["imgstate"] = 0;
            that.setData({
              list: that.data.list
            })
          }
        } else {
          wx.showToast({
            title: '拉取信息失败',
            icon: 'success',
            duration: 2000
          });
        }
      },
      fail: function (e) {
        console.log(e);
        that.data.pagestate = 1;
        that.setData({
          pagestate: 1
        });
        that.data.list = [];
        wx.showToast({
          title: '拉取信息失败',
          icon: 'success',
          duration: 2000
        });
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
