
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
