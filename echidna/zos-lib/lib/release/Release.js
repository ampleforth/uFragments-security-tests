'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _Logger = require('../utils/Logger');

var _Logger2 = _interopRequireDefault(_Logger);

var _ReleaseDeployer = require('./ReleaseDeployer');

var _ReleaseDeployer2 = _interopRequireDefault(_ReleaseDeployer);

var _Transactions = require('../utils/Transactions');

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

const log = new _Logger2.default('Release');

class Release {

  static async deployLocal(contracts, txParams = {}) {
    const deployer = new _ReleaseDeployer2.default(txParams);
    return await deployer.deployLocal(contracts);
  }

  static async deployDependency(dependencyName, contracts, txParams = {}) {
    const deployer = new _ReleaseDeployer2.default(txParams);
    return await deployer.deployDependency(dependencyName, contracts);
  }

  constructor(release, txParams = {}) {
    this._release = release;
    this.txParams = txParams;
  }

  address() {
    return this._release.address;
  }

  async owner() {
    return await this._release.owner();
  }

  async freeze() {
    log.info('Freezing release...');
    await (0, _Transactions.sendTransaction)(this._release.freeze, [], this.txParams);
  }

  async isFrozen() {
    return await this._release.frozen();
  }

  async getImplementation(contractName) {
    return await this._release.getImplementation(contractName);
  }

  async setImplementation(contractName, implementationAddress) {
    log.info(`Setting ${contractName} implementation ${implementationAddress}`);
    return await (0, _Transactions.sendTransaction)(this._release.setImplementation, [contractName, implementationAddress], this.txParams);
  }

  async unsetImplementation(contractName) {
    log.info(`Unsetting ${contractName} implementation`);
    return await (0, _Transactions.sendTransaction)(this._release.unsetImplementation, [contractName], this.txParams);
  }
}
exports.default = Release;