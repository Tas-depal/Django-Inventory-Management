/*var dynamicColors = function() {
    var r = Math.floor(Math.random() * 255);
    var g = Math.floor(Math.random() * 255);
    var b = Math.floor(Math.random() * 255);
    return "rgb(" + r + "," + g + "," + b + ")";
};
function generate_chart(order, id){
  Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';
var labels = [], data = [], colors = [];
for (var i = 0; i < order.length; i++) {
  labels.
}
// Pie Chart Example
var ctx = document.getElementById(id);
var myPieChart = new Chart(ctx, {
  type: 'pie',
  data: {
    labels: Array.from({length: order.length}, () => {}),
    datasets: [{
      data: [{% for orders in order %}'{{orders.order_quantity}}',{% endfor %}],
      backgroundColor: Array.from({length: '{{order}}'.length}, () => dynamicColors()),
      hoverBackgroundColor: Array.from({length: '{{order}}'.length}, () => dynamicColors()),
      hoverBorderColor: Array.from({length: '{{order}}'.length}, () => dynamicColors()),
    }],
  },
  options: {
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
    },
    legend: {
      display: true
    },
    cutoutPercentage: 80,
  },
});
}
*/