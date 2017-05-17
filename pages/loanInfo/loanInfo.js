// pages/loanInfo/loanInfo.js
//获取应用实例
var util = require('../../utils/util.js')
var app = getApp()
Page({
  data:{
    account: "",
    passwdMd5: "",
    loanList:[
      /*
      {"title":"01","loandate":"text1","returndate":"type1","canrenew":"1","barcode":"04400611179671"},
      {"title":"02","loandate":"text2","returndate":"type2","canrenew":"0","barcode":"04400611179671"},
      */
    ],
    pagestate: 0,
  },
  onTapRenew: function(e) {
    // 续借某书籍
    console.log(e)
    var index = e.target.id
    var barcodeNum = this.data.loanList[index].barcode;
    console.log(barcodeNum)
    var that = this;
    wx.request({
      url: "https://www.jiangfuqiang.cn/szlib/reNewBook.jsp",
      method: "POST",
      data: {
        username: this.data.account,
        password: this.data.passwdMd5,
        operation: "reNewBook",
        barcode: barcodeNum
      },
      header: {
          'content-type': 'application/x-www-form-urlencoded'
      },
      success: function(res) {
        console.log(res.data)
        if (res.statusCode == 200) {
          that.data.loanList[index].renew = "1";
          console.log(res.data.returndate)
          that.data.loanList[index].returndate = res.data.returndate
          that.setData({
            loanList: that.data.loanList
          })
          console.log(that.data.loanList)
          // 提示续借成功
          wx.showToast({
            title: '续借成功~',
            icon: 'success',
            duration: 2000
          });
        } else {
          console.log("reNewBook resp code is not 200: " + res.statusCode);
          wx.showToast({
            title: '续借失败~',
            icon: 'success',
            duration: 2000
          });
        }
      },
      fail: function(res) {
        console.log(res.data)
        console.log("reNewBook failed!")
        wx.showToast({
          title: '续借失败！',
          icon: 'success',
          duration: 2000
        })
      }
    });
  },
  onCoverLoaded: function(e) {
    var index = e.target.dataset.index;
    console.log("cover loaded: " + index);
    console.log(e);
    this.data.loanList[index]["imgstate"]=1;
    var keyStr = "loanList[" + index +"].imgstate"
    var valDict = {};
    valDict[keyStr] = "1";
    this.setData(valDict);
  },
  onCoverLoadError: function(e) {
    console.log(e);
    console.log("What's going on!!!");

    var index=e.target.dataset.index;
    this.data.loanList[index]["imgstate"] = 2;
    var keyStr = "loanList[" + index + "].imgstate"
    var valDict = {};
    valDict[keyStr] = "2";
    this.setData(valDict);

    var _errImg=e.target.dataset.errImg;
    var _errObj={};
    //_errObj[_errImg]="../../loan_book.png";
    _errObj[_errImg] = "https://www.jiangfuqiang.cn/getSzlibCover/" + this.data.loanList[index].isbn + ".jpg";
    this.data.loanList[index].img;
    console.log("reset img as: " + _errObj[_errImg]);

    //console.log( e.detail.errMsg+"----"+ _errObj[_errImg] + "----" +_errImg ); 
    this.setData(_errObj);
  },
  onTapReloadCover: function(e) {
    var index = e.target.dataset.index;
    console.log("tap cover: " + index);
    console.log(e);
    console.log(this.data.loanList);
    if (this.data.loanList[index].imgstate == 2) {
      // reset img
      var _errImg = "loanList[" + index + "].img";
      var _errObj = {};
      _errObj[_errImg] = this.data.loanList[index].img;
      //_errObj[_errImg] = "../../loan_book.png";
      console.log("reset img as: " + _errObj[_errImg]);
      console.log("----" + _errObj[_errImg] + "----" + _errImg);
      this.setData(_errObj);
    }
  },
  onLoad:function(options){
    // 页面初始化 options为页面跳转所带来的参数
    console.log(app.globalData);
    this.data.account = app.globalData.account
    this.data.passwdMd5 = app.globalData.passwdMd5
    wx.setNavigationBarTitle({
      title: '深图小助手'
    })
    // 开始拉取已借阅书籍
    var that = this;
    wx.request({
      url: 'https://www.jiangfuqiang.cn/szlib/getLoanList.jsp',
      method: "POST",
      data: {
        username: this.data.account,
        password: this.data.passwdMd5,
        operation: "getLoanList"
      },
      header: {
          'content-type': 'application/x-www-form-urlencoded'
      },
      success: function(res) {
        console.log(res)
        that.data.pagestate = 1;
        that.setData({
          pagestate: 1
        });
        if (res.statusCode == 200) {
          that.data.loanList = res.data;
          var diableAllRenewBtn = false;
          /* calculate the remain day */
          var currentdate = new Date();
          for (var index=0; index<that.data.loanList.length;index++) {
            that.data.loanList[index]["rtdate"] = util.getReturnDate(that.data.loanList[index].returndate);
            that.data.loanList[index]["remainday"] = util.getRemainDays(that.data.loanList[index].returndate);
            if (that.data.loanList[index]["remainday"] < 0) {
              diableAllRenewBtn = 1;
            }
          }
          // sort loanlist according to remainday
          that.data.loanList.sort(function(a, b){
            return (a.remainday > b.remainday);
          });
          // calculate button info
          for (var index = 0; index < that.data.loanList.length; index++) {
            var item = that.data.loanList[index];
            item["disable_btn"] = 1;
            if (item.remainday < 0) {
              item["rn_notice"] = "已过期";
            } else if (item.renew >= 1) {
              item["rn_notice"] = "已续借一次";
            } else if (diableAllRenewBtn) {
              item["rn_notice"] = "有其他未归还图书，无法续借";
            } else {
              item["disable_btn"] = 0;
            }
          }
          for (var index = 0; index < that.data.loanList.length; index++) {
            var isbn = that.data.loanList[index].isbn;
            if (index > 0) {
              (function(myIndex, myIsbn) {
                setTimeout(function() {
                  var key = "loanList[" + myIndex + "].img";
                  var coverUrl = "http://202.112.150.126/index.php?client=szlib&isbn=" + myIsbn +"/cover";
                  var currentTime = new Date();
                  console.log("currentTime: " + currentTime);
                  console.log(key + " : " + coverUrl);
                  var _errObj={};
                  _errObj[key]= coverUrl;
                  that.setData(_errObj);
                }, 100*index);
              })(index, isbn);
              that.data.loanList[index]["img"] = "";
            } else {
              that.data.loanList[index]["img"] = "http://202.112.150.126/index.php?client=szlib&isbn="+ isbn +"/cover";
            }
            that.data.loanList[index]["imgstate"] = 0;
          }
          that.setData({
            loanList: that.data.loanList
          });
        } else {
          wx.showToast({
            title: '获取借阅列表失败！',
            icon: 'success',
            duration: 2000
          });
        }
      },
      fail: function(res) {
        console.log("Fetch loan list failed" + res.data);
        that.data.pagestate = 1;
        that.setData({
          pagestate: 1
        });
        wx.showToast({
          title: '获取借阅列表失败！',
          icon: 'success',
          duration: 2000
        });
      }
    });
  },
  onTapGotoHistory: function() {
    wx.navigateTo({
      url: "../mine/info/historybooked/historybooked",
      fail: function (res) {
        // fail
      },
    });
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
