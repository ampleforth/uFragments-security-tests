'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _Logger = require('../utils/Logger');

var _Logger2 = _interopRequireDefault(_Logger);

var _Contracts = require('../utils/Contracts');

var _Contracts2 = _interopRequireDefault(_Contracts);

var _Transactions = require('../utils/Transactions');

var _App = require('./App');

var _App2 = _interopRequireDefault(_App);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

const log = new _Logger2.default('AppDeployer');

class AppDeployer {
  constructor(txParams = {}) {
    this.txParams = txParams;
  }

  async deploy(version) {
    return this.deployWithStdlib(version, 0x0);
  }

  async deployWithStdlib(version, stdlibAddress) {
    await this.createFactory();
    await this.createPackage();
    await this.createAppDirectory(stdlibAddress);
    await this.addVersion(version);
    await this.createApp(version);
    return new _App2.default(this.packagedApp, this.factory, this.appDirectory, this.package, this.version, this.txParams);
  }

  async createApp(version) {
    log.info('Deploying new PackagedApp...');
    const PackagedApp = _Contracts2.default.getFromLib('PackagedApp');
    this.packagedApp = await (0, _Transactions.deploy)(PackagedApp, [this.package.address, version, this.factory.address], this.txParams);
    log.info(`Deployed PackagedApp ${this.packagedApp.address}`);
  }

  async createFactory() {
    log.info('Deploying new UpgradeabilityProxyFactory...');
    const UpgradeabilityProxyFactory = _Contracts2.default.getFromLib('UpgradeabilityProxyFactory');
    this.factory = await (0, _Transactions.deploy)(UpgradeabilityProxyFactory, [], this.txParams);
    log.info(`Deployed UpgradeabilityProxyFactory ${this.factory.address}`);
  }

  async createPackage() {
    log.info('Deploying new Package...');
    const Package = _Contracts2.default.getFromLib('Package');
    this.package = await (0, _Transactions.deploy)(Package, [], this.txParams);
    log.info(`Deployed Package ${this.package.address}`);
  }

  async createAppDirectory(stdlibAddress) {
    log.info('Deploying new AppDirectory...');
    const AppDirectory = _Contracts2.default.getFromLib('AppDirectory');
    this.appDirectory = await (0, _Transactions.deploy)(AppDirectory, [stdlibAddress], this.txParams);
    log.info(`Deployed AppDirectory ${this.appDirectory.address}`);
  }

  async addVersion(version) {
    log.info('Adding new version...');
    this.version = version;
    await (0, _Transactions.sendTransaction)(this.package.addVersion, [version, this.appDirectory.address], this.txParams);
    log.info(`Added version ${version}`);
  }
}
exports.default = AppDeployer;