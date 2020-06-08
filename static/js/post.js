function getData() {
            var chart = echarts.init(document.getElementById('kline'), 'white', {renderer: 'canvas'});
            $.ajax({
                type: "POST",
                dataType: "json",
                url: "/Kline" ,
                data: $('#form1').serialize(),
                success: function (result) {
                    chart.setOption(result);
                },
                error: function() {
                    alert("	wrong stock code！");
                }
            });
        }