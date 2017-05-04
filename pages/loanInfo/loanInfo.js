// pages/loanInfo/loanInfo.js
//获取应用实例
var util = require('../utils/util.js')
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
    isShowPromot: false
  },
  onTapRenew: function(e) {
    // 续借某书籍
    console.log(e)
    var index = e.target.id
    var barcodeNum = this.data.loanList[index].barcode;
    console.log(barcodeNum)
    var that = this;
    wx.request({
      url: "https://www.jiangfuqiang.cn/MyLibrary/readerLoginM.jsp",
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
        console.log(res)
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
        })
      },
      fail: function(res) {
        console.log("reNewBook failed: " + res.data)
        wx.showToast({
          title: '续借失败！',
          icon: 'success',
          duration: 2000
        })
      }
    });
  },
  onLoad:function(options){
    // 页面初始化 options为页面跳转所带来的参数
    console.log(app.globalData);
    this.data.account = app.globalData.account
    this.data.passwdMd5 = app.globalData.passwdMd5
    // 开始拉取已借阅书籍
    var that = this;
    wx.request({
      url: 'https://www.jiangfuqiang.cn/MyLibrary/readerLoginM.jsp',
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
        console.log(res.data)
        console.log(res)
        if (res.statusCode == 200) {
          that.setData({
            loanList: res.data,
            isShowPromot: false
          });
          if (res.data.length==0) {
            that.setData({
              isShowPromot: true
            });
          }
          // check local cover file
          wx.getSavedFileList({
            success: function(res) {
              var localFileList = res.filelist;
              var needDownloadIsbns = new Array();
              for (var loanItem in res.data) {
                var isbn = loanItem.isbn;
                var isFind = false;
                // find out cover pictures that we do not have download yet
                for (var fileItem in localFileList) {
                  filePath = fileItem.filePath
                }
                if (isFind == false) {
                  needDownloadIsbns.push(isbn);
                }
              }
              // then download it!
              util.fetchSzlibCover({
                isbn: "978-7-301-18331-1",
                success: function(coverPath) {
                  // update UI
                }
              })
            },
            fail: function(res) {
              // fetch book cover
              util.fetchSzlibCover({
                isbn: "978-7-301-18331-1",
                success: function(coverPath) {
                  // update UI
                }
              })
            }
          });
        }
      },
      fail: function(res) {
        console.log("Fetch loan list failed" + res.data)
      }
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