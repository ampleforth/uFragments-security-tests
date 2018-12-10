'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _Package = require('./Package');

var _Package2 = _interopRequireDefault(_Package);

var _Contracts = require('../utils/Contracts');

var _Contracts2 = _interopRequireDefault(_Contracts);

var _Transactions = require('../utils/Transactions');

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

class PackageDeployer {
  constructor(txParams = {}) {
    this.txParams = txParams;
  }

  async deploy() {
    await this._createPackage();
    return new _Package2.default(this.package, this.txParams);
  }

  async _createPackage() {
    const Package = _Contracts2.default.getFromLib('Package');
    this.package = await (0, _Transactions.deploy)(Package, [], this.txParams);
  }
}
exports.default = PackageDeployer;