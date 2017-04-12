/**
 * Created by 王佳华 on 2015/7/22.
 */
//获得当前时间  yyyy-mm-dd H:i:s
function getLocalTime(){
    localTime=new Date();
    var month=localTime.getMonth()+1;
    var strTime=localTime.getFullYear()+'-'+ month +'-'+localTime.getDate()+' '+ localTime.getHours() + ':' +localTime.getMinutes()+':'+localTime.getSeconds();
    return strTime;
}
function LineTable(select,measure_datetime,systolic_pressure,diastolic_pressure,heart_rate){
    $('#'+select).highcharts({
        title: {
            text: '血压/心率趋势图'
        },
        subtitle: {
            text: null
        },
        xAxis: {
            categories:measure_datetime,
            gridLineWidth:1,
            type: 'datetime'
        },
        yAxis: [{ // left y axis
            title: {
            text: '血压(mmHg)'
            },
            labels: {
                align: 'left',
                x: 3,
                y: 16,
                format: '{value:.,0f}'
            },
            showFirstLabel: true
        }, { // right y axis
            gridLineWidth: 0,
            opposite: true,
            title: {
                text: '心率(次/分)'
            },
            labels: {
                align: 'right',
                x: -3,
                y: 16,
                format: '{value:.,0f}'
            },
            showFirstLabel: true
        }],
        legend: {
            align: 'left',
            verticalAlign: 'top',
            y: 20,
            floating: true,
            borderWidth: 0
        },
        tooltip: {
            shared: true,
            crosshairs: true
        },
        series: [{
            name: '收缩压',
            lineWidth: 4,
            yAxis:0,
            data:systolic_pressure
        }, {
            name: '舒张压',
            lineWidth: 4,
            yAxis:0,
            data:diastolic_pressure
        },{
            name: '心率',
            lineWidth: 4,
            yAxis:1,
            data:heart_rate
        }],
        credits:{
            enabled:true,
            href:'http://http://eis.whu.edu.cn/',
            text:'武汉大学-光谱成像实验室'
        }
    });
}
function LineTable1(select,measure_datetime,gluocose){
    $('#'+select).highcharts({
        title: {
            text: '血糖趋势图'
        },
        subtitle: {
            text: null
        },
        xAxis: {
            categories:measure_datetime,
            gridLineWidth:1,
            type: 'datetime'
        },
        yAxis: [{ // left y axis
            title: {
            text: '血糖(mg/dl)'
            },
            labels: {
                align: 'left',
                x: 3,
                y: 16,
                format: '{value:.,0f}'
            },
            showFirstLabel: true
        }],
        legend: {
            align: 'left',
            verticalAlign: 'top',
            y: 20,
            floating: true,
            borderWidth: 0
        },
        tooltip: {
            shared: true,
            crosshairs: true
        },
        series: [{
            name: '血糖',
            lineWidth: 4,
            yAxis:0,
            data:gluocose
        }],
        credits:{
            enabled:true,
            href:'http://http://eis.whu.edu.cn/',
            text:'武汉大学-光谱成像实验室'
        }
    });
}
function LineTable2(select,measure_datetime,gluocose){
    $('#'+select).highcharts({
        title: {
            text: '体温趋势图'
        },
        subtitle: {
            text: null
        },
        xAxis: {
            categories:measure_datetime,
            gridLineWidth:1,
            type: 'datetime'
        },
        yAxis: [{ // left y axis
            title: {
            text: '体温(摄氏度)'
            },
            labels: {
                align: 'left',
                x: 3,
                y: 16,
                format: '{value:.,0f}'
            },
            showFirstLabel: true
        }],
        legend: {
            align: 'left',
            verticalAlign: 'top',
            y: 20,
            floating: true,
            borderWidth: 0
        },
        tooltip: {
            shared: true,
            crosshairs: true
        },
        series: [{
            name: '体温',
            lineWidth: 4,
            yAxis:0,
            data:gluocose
        }],
        credits:{
            enabled:true,
            href:'http://http://eis.whu.edu.cn/',
            text:'武汉大学-光谱成像实验室'
        }
    });
}
function LineTable3(select,measure_datetime,gluocose){
    $('#'+select).highcharts({
        title: {
            text: '干式荧光仪数据趋势图'
        },
        subtitle: {
            text: null
        },
        xAxis: {
            categories:measure_datetime,
            gridLineWidth:1,
            type: 'datetime'
        },
        yAxis: [{ // left y axis
            title: {
            text: '干式荧光仪数据'
            },
            labels: {
                align: 'left',
                x: 3,
                y: 16,
                format: '{value:.,0f}'
            },
            showFirstLabel: true
        }],
        legend: {
            align: 'left',
            verticalAlign: 'top',
            y: 20,
            floating: true,
            borderWidth: 0
        },
        tooltip: {
            shared: true,
            crosshairs: true
        },
        series: [{
            name: '干式荧光仪数据',
            lineWidth: 4,
            yAxis:0,
            data:gluocose
        }],
        credits:{
            enabled:true,
            href:'http://http://eis.whu.edu.cn/',
            text:'武汉大学-光谱成像实验室'
        }
    });
}