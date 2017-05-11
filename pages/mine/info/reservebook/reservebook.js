// pages/mine/info/reservebook/reservebook.js
var util = require('../../../../utils/util.js')
var app = getApp()
Page({
  data:{
    list: [
    ]
  },
  onCoverLoadError: function (e) {
    console.log(e);
    console.log("What's going on!!!");

    var index = e.target.dataset.index;
    var _errImg = e.target.dataset.errImg;
    var _errObj = {};
    _errObj[_errImg] = "../../loan_book.png";
    //_errObj[_errImg]=this.data.loanList[index].img;
    console.log("reset img as: " + _errObj[_errImg]);

    console.log(e.detail.errMsg + "----" + _errObj[_errImg] + "----" + _errImg);
    var that = this;
    setTimeout(function () {
        that.setData(_errObj);
      },
      400
    );
  },
  onTapReloadCover: function (e) {
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
            that.data.list[index]["img"] = "../../wechat_gray.jpg";
          } else {
            that.data.list[index]["img"] = "http://202.112.150.126/index.php?client=szlib&isbn="+ isbn +"/cover";
          }
          that.setData({
            list: that.data.list
          })
        }
      },
      fail: function (e) {
        console.log(e);
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
