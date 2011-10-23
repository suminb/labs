var _data = [
    ['Firefox',   45.0],
    ['IE',       26.8],
    {
        name: 'Chrome',    
        y: 12.8,
        sliced: true,
        selected: true
    },
    ['Safari',    8.5],
    ['Opera',     6.2],
    ['Others',   0.7]
];

/**
 * http://stackoverflow.com/questions/18912/how-to-find-keys-of-a-hash
 *
Object.prototype.keys = function () {
    var keys = [];
    for(var i in this) if (this.hasOwnProperty(i)) {
        keys.push(i);
    }
    return keys;
}

Object.prototype.values = function() {
    var values = [];
    for(var k in this) {
        if(this.hasOwnProperty(k)) values.push(this[k]);
    }
    return values;
}
*/