var charts = {};
var drawFunctions = {
'chart-slow-by-vehicle-year': function() {
    if(charts['chart-slow-by-vehicle-year'] == null)
    charts['chart-slow-by-vehicle-year'] = new Highcharts.Chart({
        chart: {
            renderTo: 'chart-slow-by-vehicle-year',
            defaultSeriesType: 'column'
        },
        title: {
            text: 'Probabilistic distribution by vehicle year'
        },
        /*
        subtitle: {
            text: ''
        },
        */
        xAxis: {
            categories: slowByVehicleYear.map(function(x) {return x[0]})
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Probability'
            },
            labels: {
                formatter: function() {
                    return $.sprintf('%.2f %%', this.value*100);
                }
            }
        },
        legend: {
            layout: 'vertical',
            backgroundColor: '#FFFFFF',
            align: 'left',
            verticalAlign: 'top',
            x: 100,
            y: 70,
            floating: true,
            shadow: true
        },
        tooltip: {
            formatter: function() {
                return $.sprintf('<b>%d</b>: %.02f %%', this.x, this.y*100);
            }
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [{
            name: 'Slow',
            data: slowByVehicleYear.map(function(x) {return x[1]})
        },
        {
            name: 'Fast',
            data: fastByVehicleYear.map(function(x) {return x[1]})
        }]
    });
},
'chart-slow-by-vehicle-make': function() {
    if(charts['chart-slow-by-vehicle-make'] == null)
    charts['chart-slow-by-vehicle-make'] =  new Highcharts.Chart({
        chart: {
            renderTo: 'chart-slow-by-vehicle-make',
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false
        },
        title: {
            text: 'Slow drivers by vehicle manufacturer'
        },
        tooltip: {
            formatter: function() {
                return $.sprintf('<b>%s</b> %.1f %%', this.point.name, this.percentage);
            }
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    color: '#000000',
                    connectorColor: '#000000',
                    formatter: function() {
                        return $.sprintf('<b>%s</b>', this.point.name);
                    }
                }
            }
        },
        series: [{
            type: 'pie',
            name: 'Browser share',
            data: byMake
        }]
    });
},
'chart-slow-by-vehicle-body-type': function() {
    if(charts['chart-slow-by-vehicle-body-type'] == null)
    charts['chart-slow-by-vehicle-body-type'] = new Highcharts.Chart({
        chart: {
            renderTo: 'chart-slow-by-vehicle-body-type',
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false
        },
        title: {
            text: 'Slow drivers by body type'
        },
        tooltip: {
            formatter: function() {
                return $.sprintf('<b>%s</b> %.1f %%', this.point.name, this.percentage);
            }
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    color: '#000000',
                    connectorColor: '#000000',
                    formatter: function() {
                        return $.sprintf('<b>%s</b>', this.point.name);
                    }
                }
            }
        },
        series: [{
            type: 'pie',
            name: '',
            data: byBodyType
        }]
    });
},
'chart-slow-by-vehicle-color': function() {
    if(charts['chart-slow-by-vehicle-color'] == null)
    charts['chart-slow-by-vehicle-color'] = new Highcharts.Chart({
        chart: {
            renderTo: 'chart-slow-by-vehicle-color',
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false
        },
        title: {
            text: 'Slow drivers by vehicle color'
        },
        tooltip: {
            formatter: function() {
                return $.sprintf('<b>%s</b> %.1f %%', this.point.name, this.percentage);
            }
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    color: '#000000',
                    connectorColor: '#000000',
                    formatter: function() {
                        return $.sprintf('<b>%s</b>', this.point.name);
                    }
                }
            }
        },
        series: [{
            type: 'pie',
            name: '',
            data: byColor
        }]
    });
},
'chart-slow-by-driver-age': function() {
    if(charts['chart-slow-by-driver-age'] == null)
    charts['chart-slow-by-driver-age'] = new Highcharts.Chart({
        chart: {
            renderTo: 'chart-slow-by-driver-age',
            defaultSeriesType: 'column'
        },
        title: {
            text: 'Probabilistic distribution by driver age'
        },
        xAxis: {
            categories: slowByDriverAge.map(function(x) {return x[0]})
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Probability'
            },
            labels: {
                formatter: function() {
                    return $.sprintf('%.02f %%', this.value*100);
                }
            }
        },
        legend: {
            layout: 'vertical',
            backgroundColor: '#FFFFFF',
            align: 'left',
            verticalAlign: 'top',
            x: 100,
            y: 70,
            floating: true,
            shadow: true
        },
        tooltip: {
            formatter: function() {
                return $.sprintf('<b>%d</b>: %.02f %%', this.x, this.y*100);
            }
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [{
            name: 'Slow',
            data: slowByDriverAge.map(function(x) {return x[1]})
        },
        {
            name: 'Fast',
            data: fastByDriverAge.map(function(x) {return x[1]})
        }]
    });
}
};