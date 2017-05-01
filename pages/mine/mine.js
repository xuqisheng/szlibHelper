// pages/mine/mine.js
Page({
  data:{
    list: [
      {
        id: 'finance',
        name: '我的财经',
        open: false
      }, {
        id: 'libary_info',
        name: '我的读者证',
        open: false
      }, {
        id: 'person_info',
        name: '个人信息',
        open: false
      }, {
        id: 'prebooked',
        name: '我的预借',
        open: false
      }, {
        id: 'logout',
        name: '退出登录',
        open: false
      }
    ]
  },
  kindToggle: function (e) {
    var id = e.currentTarget.id, list = this.data.list;
  },
  onLoad:function(options){
    // 页面初始化 options为页面跳转所带来的参数
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