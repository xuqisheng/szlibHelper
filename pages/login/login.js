//login.js
//获取应用实例
var app = getApp()
Page({
  data: {
    account: "",
    passwd: "",
    isChecked: 1,
    userInfo: {}
  },
  // 响应账号输入
  bindAccountInput: function(e) {
    //var account = "0440050867306"
    this.setData({
      account:e.detail.value
    });
  },
  // 响应密码输入
  bindPasswordInput: function(e) {
    this.setData({
      passwd:e.detail.value
    });
  },
  // 响应单选框变化
  checkboxChange: function(e) {
    console.log(e);
    var selected = e.detail.value.length>0? true: false;
    this.setData({
      isChecked:selected
    });
    console.log("checkbox: " + selected);
  },
  // 点击登录
  onTapLogin: function() {
    console.log(this.data.account);
    console.log(this.data.passwd);
    // 判空提示
    if (this.data.account.length==0) {
      wx.showToast({
        title: '账号不能为空~',
        icon: 'success',
        duration: 2000
      })
      return;
    }
    if (this.data.passwd.length==0) {
      wx.showToast({
        title: '密码不能为空~',
        icon: 'success',
        duration: 2000
      })
      return;
    }
    var md5Tool = require('../../utils/myMD5.js');
    var passwd_md5 = md5Tool.hexMD5(this.data.passwd);
    console.log(passwd_md5);
    var that = this;
    wx.request({
      url: 'https://www.jiangfuqiang.cn/szlib/login.jsp',
      method: "POST",
      data: {
        username: this.data.account,
        password: passwd_md5,
        operation: "login"
      },
      header: {
          'content-type': 'application/x-www-form-urlencoded'
      },
      success: function(res) {
        console.log(res)
        if (res.statusCode == 200) {
          wx.switchTab({
            url: "../loanInfo/loanInfo"
          })
        } else {
          // 提醒失败
          var message = "登录失败!";
          if (res.data.message) {
            message = res.data.message;
          }
          wx.showToast({
            title: message,
            icon: 'success',
            duration: 2000
          });
        }
        // 将通用信息保存在全局 app 中
        app.globalData.account = that.data.account;
        app.globalData.passwdMd5 = passwd_md5;
      },
      fail: function(res) {
        console.log("Login failed" + res.data)
        wx.showToast({
          title: '网络错误！',
          icon: 'success',
          duration: 2000
        });
      },
      complete: function(res) {
        // check whether to store or update account info to storage
        if (that.data.isChecked) {
          wx.setStorage({
            key: "account",
            data: that.data.account
          });
          wx.setStorage({
            key: "passwd",
            data: that.data.passwd
          });
        }
        wx.setStorage({
          key: "isChecked",
          data: that.data.isChecked
        });
      }
    });
  },
  // 响应调用扫描
  onTapScan: function() {
    var that = this;
    wx.scanCode({
      success: (res) => {
        console.log(res)
        that.setData({
          account: res.result
        })
      },
      failed: (res) => {
        console.log(res)
      },
      complete: (res) => {
        console.log(res)
      }
    })
  },
  onLoad: function () {
    var that = this
    wx.getStorage({
      key: 'account',
      success: function(res) {
          console.log(res.data)
          that.setData({
            account: res.data
          })
      } 
    });
    wx.getStorage({
      key: 'passwd',
      success: function(res) {
          console.log(res.data)
          that.setData({
            passwd: res.data
          })
      } 
    });
    wx.getStorage({
      key: 'isChecked',
      success: function(res) {
          console.log(res.data)
          that.setData({
            isChecked: res.data
          })
      }
    });
  }
})
