// pages/mine/info/generalInfo.js
var util = require('../../../utils/util.js')
var app = getApp()
Page({
  data:{
    list: [
      {
        section_name: "default_section",
        data: [{
          name: "姓名",
          value: "张三"
        },
        {
          name: "可借数量",
          value: "10本"
        }]
      },
      {
        section_name: "second_section",
        data: [{
          name: "有效期",
          value: "2020-05-01"
        },
        {
          name: "状态",
          value: "有效"
        }]
      }
    ]
  },
  onLoad:function(options){
    // 页面初始化 options为页面跳转所带来的参数
    console.log(options);
    console.log("here is the generalInfo page!");
    var page = options.page;
    var readerData = app.globalData.readerData;
    if (page == "finance") {
      this.data.list = [
        {
          section_name: "default_section",
          data: [{
            name: "总欠款",
            value: "￥ " + readerData.arrea
          },
          {
            name: "总押金",
            value: "￥ " + readerData.deposit
          },
          {
            name: "总预付款",
            value: "￥ " + readerData.banlance
          }]
        }
      ]
    } else if (page == "libary_info") {
      this.data.list = [
        {
          section_name: "sec_card_info",
          data: [{
            name: "类型",
            value: readerData.CardType
          },
          {
            name: "读者证号",
            value:  readerData.Cardno
          },
          {
            name: "有效期截至到",
            value: readerData.CardEnddate
          },
          {
            name: "状态",
            value: readerData.Status
          }
          ]
        },
        {
          section_name: "sec_card_abilities",
          data: [{
            name: "可外借图书",
            value: readerData.canloannum + "本"
          },
          {
            name: "可上机时间",
            value:  "120分钟"
          },
          {
            name: "无线WiFi服务",
            value: "开通"
          },
          {
            name: "统一服务",
            value: "开通"
          },
          {
            name: "预借服务",
            value: "开通"
          }
          ]
        }
      ]
    }
    this.setData({
      data: this.data
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