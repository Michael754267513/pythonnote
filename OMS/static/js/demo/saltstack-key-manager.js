$(function () {

    //var polarChart = document.getElementById("polarChart");
    //var polarData = {
    //    datasets: [{
    //        data: polarChart.getAttribute('value').split(' '),
    //        backgroundColor: [
    //            "#a3e1d4", "#dedede", "#b5b8cf"
    //        ],
    //        label: [
    //            "My Radar chart"
    //        ]
    //    }],
    //    labels: [
    //        "用户组","用户","业务组"
    //    ]
    //};
    //
    //var polarOptions = {
    //    segmentStrokeWidth: 2,
    //    responsive: true
    //
    //};

    //var ctx3 = polarChart.getContext("2d");
    //new Chart(ctx3, {type: 'pie', data: polarData, options:polarOptions});


    var doughnutChart = document.getElementById("doughnutChart");
    var doughnutData = {
        labels: ["accepted_num","denied_num"],
        datasets: [{
            data: doughnutChart.getAttribute('value').split(' '),
            //data: [1,0,0,0],
            backgroundColor: ["#a3e1d4","#F38630"]
        }]
    } ;


    var doughnutOptions = {
        responsive: true
    };


    var ctx4 = document.getElementById("doughnutChart").getContext("2d");
    new Chart(ctx4, {type: 'doughnut', data: doughnutData, options:doughnutOptions});


    var doughnutChart1 = document.getElementById("doughnutChart1");
    var doughnutData1 = {
        labels: ["pre_num","rejected_num"],
        datasets: [{
            data: doughnutChart1.getAttribute('value').split(' '),
            //data: [1,0,0,0],
            backgroundColor: ["#a3e1d4","#F38630"]
        }]
    } ;


    var doughnutOptions1 = {
        responsive: true
    };


    var ctx1 = document.getElementById("doughnutChart1").getContext("2d");
    new Chart(ctx1, {type: 'doughnut', data: doughnutData1, options:doughnutOptions1});



});