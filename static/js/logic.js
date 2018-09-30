
function start() {
    var input_ = document.getElementById('start').value
    console.log(input_)
    d3.json(`/api/v1.0/${input_}`)
    .then(function(data) {d3.select('#data').html(data["Average Temperature"])})
}

