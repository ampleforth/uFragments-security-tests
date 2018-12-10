'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _util = require('util');

class Proxy {
  static at(address) {
    return new Proxy(address);
  }

  constructor(address) {
    this.address = address;
  }

  async implementation() {
    const position = web3.sha3('org.zeppelinos.proxy.implementation');
    return this.getStorageAt(position);
  }

  async admin() {
    const position = web3.sha3('org.zeppelinos.proxy.admin');
    return this.getStorageAt(position);
  }

  async getStorageAt(position) {
    return (0, _util.promisify)(web3.eth.getStorageAt.bind(web3.eth))(this.address, position);
  }
}
exports.default = Proxy;