/**
 * Created by hao.ren3 on 2019/12/27.
 */

function f_echarts_line_chart(div_id, date, data, min_cnt, max_cnt, interval) {
    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.getElementById(div_id));

    // 指定图表的配置项和数据
    var option = {
        tooltip: {
            trigger: 'axis',
            position: function (pt) {
                return [pt[0], '10%'];
            }
        },
        title: {
            left: 'center',
            text: '每日投票人数统计'
        },
        toolbox: {
            feature: {
                dataZoom: {
                    yAxisIndex: 'none'
                },
                restore: {},
                saveAsImage: {}
            }
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: date
        },
        yAxis: {
            type: 'value',
            min: min_cnt,
            max: max_cnt,
            interval: interval,
            boundaryGap: [0, '100%']
        },
        dataZoom: [{
            type: 'inside',
            start: 0,
            end: 100
        }, {
            start: 0,
            end: 100,
            handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
            handleSize: '80%',
            handleStyle: {
                color: '#fff',
                shadowBlur: 3,
                shadowColor: 'rgba(0, 0, 0, 0.6)',
                shadowOffsetX: 2,
                shadowOffsetY: 2
            }
        }],
        series: [
            {
                name:'投票人数',
                type:'line',
                smooth:true,
                symbol: 'none',
                sampling: 'average',
                itemStyle: {
                    color: 'rgb(255, 70, 131)'
                },
                areaStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                        offset: 0,
                        color: 'rgb(255, 158, 68)'
                    }, {
                        offset: 1,
                        color: 'rgb(255, 70, 131)'
                    }])
                },
                data: data
            }
        ]
    };

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}

function f_echarts_radar(div_id, names2, data2) {
            var myChart2 = echarts.init(document.getElementById(div_id));
            // 指定图表的配置项和数据
            var option2 = {
                title: {
                    text: '投票统计',
                    left: 0,
                    top: 10,
                    textStyle: {
                        color: '#323232'
                    }
                },
                tooltip: {
                    trigger: 'item',
                    backgroundColor : 'rgba(0,0,250,0.2)'
                },
                radar: {indicator : names2},
                series : [{
                    name:'投票人',
                    type: 'radar',
                    symbol: 'none',
                    lineStyle: {
                        width: 1
                    },
                    emphasis: {
                        areaStyle: {
                            color: 'rgba(0,250,0,0.3)'
                        }
                    },
                    data:[
                      {
                        value:data2
                      }
                    ]
                }]
            };

            // 使用刚指定的配置项和数据显示图表。
            myChart2.setOption(option2);
        }

function vote_for_topic(vote_id, option_id, user_id) {
    window.location.href="/act/vote/add/"+vote_id+"/"+option_id+"/"+user_id;
}

function delete_select(vote_id, user_id) {
    window.location.href="/act/vote/delete/"+vote_id+"/"+user_id;
}

function change_vote(vote_id, option_id, user_id) {
    if (window.confirm("您确认要修改您的选择？")){
        window.location.href="/act/vote/change/"+vote_id+"/"+option_id+"/"+user_id;
    }
}

function get_restaurant_id(restaurant_string) {
    return restaurant_string.split("：")[0]
}

function get_restaurant_name(restaurant_string) {
    return restaurant_string.split("：")[1]
}