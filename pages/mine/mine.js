// pages/mine/mine.js
Page({
  data:{
    list: [
      {
        id: 'historbooked',
        name: '历史借阅',
        open: false,
        page: '../info/historybooked/historybooked'
      }, {
        id: 'reservebook',
        name: '我的预借',
        open: false,
        page: '../reservebook/reservebook'
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
    var id = e.currentTarget.id, list = this.data.list;
    var index = e.currentTarget.dataset.index;
    if (id=='logout') {
      wx.reLaunch({
        url: list[index].page,
      });
    } else if (id== 'finance' || id == 'libary_info') {
      wx.navigateTo({
        url: "info/generalInfo?page=" + id,
        fail: function(res) {
          // fail
        },
      });
    } else if (id == 'historbooked') {
    } else if (id == 'reservebook') {

    }
  },
  onLoad:function(options){
    // 页面初始化 options为页面跳转所带来的参数
    // get reader info
    wx.request({
      url: 'https://www.jiangfuqiang.cn/szlib/readerinfo.jsp',
      data: {
        username: app.globalData.account,
        password: app.globalData.passwdMd5,
        operation: "getReaderInfo"
      },
      method: 'POST',
      success: function(res){
        // success
        console.log(res.data);
        app.readerData = res.data;
      },
      fail: function(res) {
        // fail
        console.log(res);
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