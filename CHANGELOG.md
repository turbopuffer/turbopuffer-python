# Changelog

## 0.5.11 (2025-07-09)

Full Changelog: [v0.5.10...v0.5.11](https://github.com/turbopuffer/turbopuffer-python/compare/v0.5.10...v0.5.11)

### Bug Fixes

* **api:** api update ([4ea9eda](https://github.com/turbopuffer/turbopuffer-python/commit/4ea9eda6acd86390dc223c0224d76c594776cacc))
* don't require region unless baseUrl contains {region} placeholder ([#137](https://github.com/turbopuffer/turbopuffer-python/issues/137)) ([b63b7c8](https://github.com/turbopuffer/turbopuffer-python/commit/b63b7c81854479a7644e66a843fa7794b67d41c2))


### Chores

* **internal:** bump pinned h11 dep ([4f70ea2](https://github.com/turbopuffer/turbopuffer-python/commit/4f70ea23a2ae016006e6a90e625de6b9b8884453))
* **package:** mark python 3.13 as supported ([7e91954](https://github.com/turbopuffer/turbopuffer-python/commit/7e919541aa45a494a021fd5728b792b7f048eb19))

## 0.5.10 (2025-07-07)

Full Changelog: [v0.5.9...v0.5.10](https://github.com/turbopuffer/turbopuffer-python/compare/v0.5.9...v0.5.10)

### Bug Fixes

* **api:** add support for [Not]Contains[Any] operators ([#135](https://github.com/turbopuffer/turbopuffer-python/issues/135)) ([286db87](https://github.com/turbopuffer/turbopuffer-python/commit/286db871a4c558d74fd34103fefd7b915b9bb1c7))
* **api:** api update ([afecdd0](https://github.com/turbopuffer/turbopuffer-python/commit/afecdd0bbcbf0a8b40f1d6802a55fc4ecb24128e))


### Chores

* **ci:** change upload type ([99ba1aa](https://github.com/turbopuffer/turbopuffer-python/commit/99ba1aa8c8f208de772e8bd5f9ef955726a89280))

## 0.5.9 (2025-07-01)

Full Changelog: [v0.5.8...v0.5.9](https://github.com/turbopuffer/turbopuffer-python/compare/v0.5.8...v0.5.9)

### Features

* **client:** add support for aiohttp ([4d58a72](https://github.com/turbopuffer/turbopuffer-python/commit/4d58a72dcc7a4209911c8bc69c1aa8abec38486b))


### Bug Fixes

* add support for `$ref_new` expressions ([#132](https://github.com/turbopuffer/turbopuffer-python/issues/132)) ([943228e](https://github.com/turbopuffer/turbopuffer-python/commit/943228e59158468f13a2002cc4446211cf03a639))
* **api:** api update ([303f8bb](https://github.com/turbopuffer/turbopuffer-python/commit/303f8bb649c66fad8f1331d0cd32016403b091d5))
* **api:** api update ([e8fee42](https://github.com/turbopuffer/turbopuffer-python/commit/e8fee42be99526a9015ae7cebd3b78d78dfe1ff6))
* **ci:** correct conditional ([13b08d9](https://github.com/turbopuffer/turbopuffer-python/commit/13b08d964844351835d1d256524675544002653e))
* **ci:** release-doctor — report correct token name ([9ca4a70](https://github.com/turbopuffer/turbopuffer-python/commit/9ca4a70480d6536d37815ca96f790a60cc37f97d))
* correct name of stainless bot ([#133](https://github.com/turbopuffer/turbopuffer-python/issues/133)) ([acab273](https://github.com/turbopuffer/turbopuffer-python/commit/acab273999c22ec0719b7f8d8e25eeaf219279f0))
* **README:** improve headline example ([#131](https://github.com/turbopuffer/turbopuffer-python/issues/131)) ([7db0fb2](https://github.com/turbopuffer/turbopuffer-python/commit/7db0fb229944b040de5b8da0dc6389358d70804d))
* strict types for write conditions ([#130](https://github.com/turbopuffer/turbopuffer-python/issues/130)) ([75c4515](https://github.com/turbopuffer/turbopuffer-python/commit/75c45150da8f183bdcddb70ab142d4eeed17a218))


### Chores

* **ci:** only run for pushes and fork pull requests ([4e928d3](https://github.com/turbopuffer/turbopuffer-python/commit/4e928d310d7ba1022850ced923625c9d869ee73d))
* **tests:** skip some failing tests on the latest python versions ([d2c4814](https://github.com/turbopuffer/turbopuffer-python/commit/d2c4814ee0c3f9dcccd97b64d3c186242c18a9d7))

## 0.5.8 (2025-06-20)

Full Changelog: [v0.5.7...v0.5.8](https://github.com/turbopuffer/turbopuffer-python/compare/v0.5.7...v0.5.8)

### Features

* **api:** introduce dedicated Query model ([bc09dc2](https://github.com/turbopuffer/turbopuffer-python/commit/bc09dc28b8a548ae9a06b2cb54e3698e37e563df))


### Bug Fixes

* strict types for new QueryParam type ([fae8c4d](https://github.com/turbopuffer/turbopuffer-python/commit/fae8c4d7f79d52f7996c1638492b28b9b72874aa))


### Chores

* **readme:** update badges ([d03eb1a](https://github.com/turbopuffer/turbopuffer-python/commit/d03eb1a5e6be5f24219f40e1274dba253c15c327))


### Documentation

* **client:** fix httpx.Timeout documentation reference ([320cee5](https://github.com/turbopuffer/turbopuffer-python/commit/320cee594b3984151dd589d38d872bf287f240ad))

## 0.5.7 (2025-06-19)

Full Changelog: [v0.5.6...v0.5.7](https://github.com/turbopuffer/turbopuffer-python/compare/v0.5.6...v0.5.7)

### Bug Fixes

* strict types for async query and multi_query APIs ([#127](https://github.com/turbopuffer/turbopuffer-python/issues/127)) ([a5d2982](https://github.com/turbopuffer/turbopuffer-python/commit/a5d2982bd4fcc5cdd3e585a3ebc1f19158082cb6))


### Chores

* **ci:** enable for pull requests ([d975004](https://github.com/turbopuffer/turbopuffer-python/commit/d975004fda35132fd9b580e06c8bf0ab9a27a4ae))
* **internal:** update conftest.py ([50476ac](https://github.com/turbopuffer/turbopuffer-python/commit/50476ac2de7ea6b0b7443d23f24ad1ab2b4529c1))
* **tests:** add tests for httpx client instantiation & proxies ([a44fc4f](https://github.com/turbopuffer/turbopuffer-python/commit/a44fc4f90fa597dc86fa2222d84183996adce109))

## 0.5.6 (2025-06-16)

Full Changelog: [v0.5.5...v0.5.6](https://github.com/turbopuffer/turbopuffer-python/compare/v0.5.5...v0.5.6)

### Bug Fixes

* don't run grouped tests in parallel ([#125](https://github.com/turbopuffer/turbopuffer-python/issues/125)) ([9024587](https://github.com/turbopuffer/turbopuffer-python/commit/902458767faf238a7fd9bb012bf7026dc2a83a3b))

## 0.5.5 (2025-06-15)

Full Changelog: [v0.5.4...v0.5.5](https://github.com/turbopuffer/turbopuffer-python/compare/v0.5.4...v0.5.5)

### Bug Fixes

* remove type annotation that's invalid in Python 3.8 ([#123](https://github.com/turbopuffer/turbopuffer-python/issues/123)) ([8dddad5](https://github.com/turbopuffer/turbopuffer-python/commit/8dddad5cbb0b76ec64f07ef92795f6c1a8b60423))

## 0.5.4 (2025-06-15)

Full Changelog: [v0.5.3...v0.5.4](https://github.com/turbopuffer/turbopuffer-python/compare/v0.5.3...v0.5.4)

### Bug Fixes

* **client:** correctly parse binary response | stream ([aa37450](https://github.com/turbopuffer/turbopuffer-python/commit/aa37450a59f799ad9ce2b7eabe6f540faad1ecbd))
* restore support for Python 3.8 ([#121](https://github.com/turbopuffer/turbopuffer-python/issues/121)) ([d751354](https://github.com/turbopuffer/turbopuffer-python/commit/d751354ae32b7331e822cddeda1584105196930f))


### Chores

* **tests:** run tests in parallel ([687c922](https://github.com/turbopuffer/turbopuffer-python/commit/687c9228f2d38be8a5c231753fd998938b1bb86f))

## 0.5.3 (2025-06-12)

Full Changelog: [v0.5.2...v0.5.3](https://github.com/turbopuffer/turbopuffer-python/compare/v0.5.2...v0.5.3)

### Bug Fixes

* mark urllib3 optional ([#118](https://github.com/turbopuffer/turbopuffer-python/issues/118)) ([85ab0de](https://github.com/turbopuffer/turbopuffer-python/commit/85ab0deef64843b47bc33bce267a098a11006355))

## 0.5.2 (2025-06-11)

Full Changelog: [v0.5.1...v0.5.2](https://github.com/turbopuffer/turbopuffer-python/compare/v0.5.1...v0.5.2)

### Bug Fixes

* **docs:** add note about attribute flattening to upgrade guide ([#115](https://github.com/turbopuffer/turbopuffer-python/issues/115)) ([568348d](https://github.com/turbopuffer/turbopuffer-python/commit/568348dc7e3a06dcdcd59aa488c346f2c717ffa3))
* **tests:** mock delete when testing namespace default params ([#116](https://github.com/turbopuffer/turbopuffer-python/issues/116)) ([db587e8](https://github.com/turbopuffer/turbopuffer-python/commit/db587e860af7951d8549a70cff86c93e9f6259ca))


### Chores

* prepare for release ([89006af](https://github.com/turbopuffer/turbopuffer-python/commit/89006afdb329c74cd7d91e857c86aaed9a065696))

## 0.5.1 (2025-06-11)

Full Changelog: [v0.5.0...v0.5.1](https://github.com/turbopuffer/turbopuffer-python/compare/v0.5.0...v0.5.1)

### Bug Fixes

* **api:** add support for new multi-query api
* **tests:** mock delete whne testing namespace default params ([072f33a](https://github.com/turbopuffer/turbopuffer-python/commit/072f33a9758fcfc20cad675971f6efb91aba7b00))


### Chores

* **internal:** codegen related update ([5fa49e7](https://github.com/turbopuffer/turbopuffer-python/commit/5fa49e77a0167caea75dd9abc22c63b5779d8bc1))
* sync repo ([3f7d6f7](https://github.com/turbopuffer/turbopuffer-python/commit/3f7d6f72db281f013bbe3fc4ff1e56392d61fd05))

## 0.5.0 (2025-06-10)

Full Changelog: [v0.5.0-alpha.15...v0.5.0](https://github.com/turbopuffer/turbopuffer-python/compare/v0.5.0-alpha.15...v0.5.0)

### Features

* improve performance with custom transports ([#111](https://github.com/turbopuffer/turbopuffer-python/issues/111)) ([7def3c6](https://github.com/turbopuffer/turbopuffer-python/commit/7def3c64a5664b616a53b560252839ef36fbd010))


### Bug Fixes

* **README:** align docs link with other SDKs ([91b8b69](https://github.com/turbopuffer/turbopuffer-python/commit/91b8b698a3ac76a40b94646cf49ece9e94f79b8d))

## 0.5.0-alpha.15 (2025-06-09)

Full Changelog: [v0.5.0-alpha.14...v0.5.0-alpha.15](https://github.com/turbopuffer/turbopuffer-python/compare/v0.5.0-alpha.14...v0.5.0-alpha.15)

### Features

* improve deprecation warnings ([b38de2e](https://github.com/turbopuffer/turbopuffer-python/commit/b38de2eb4e063b0d9534862cfc517764ca1f56b1))


### Bug Fixes

* typings of deprecation warnings ([e0c7e8a](https://github.com/turbopuffer/turbopuffer-python/commit/e0c7e8a5688540d5ffecbc0fdcc1295530a8e19d))

## 0.5.0-alpha.14 (2025-06-09)

Full Changelog: [v0.5.0-alpha.13...v0.5.0-alpha.14](https://github.com/turbopuffer/turbopuffer-python/compare/v0.5.0-alpha.13...v0.5.0-alpha.14)

### Features

* add deprecation shims ([cfd1438](https://github.com/turbopuffer/turbopuffer-python/commit/cfd14380cf584c5c96b5d414cc8e417f89b20643))
* add Namespace.exists() async method ([117c3f0](https://github.com/turbopuffer/turbopuffer-python/commit/117c3f0be2d016a11c94844cacae25faca67f566))
* restore Namespace.exists() method ([c6f2f9c](https://github.com/turbopuffer/turbopuffer-python/commit/c6f2f9cd4c3340eb6208260ac69c6cbe0642d206))


### Bug Fixes

* specify distance_metric in exists tests ([f52ac9b](https://github.com/turbopuffer/turbopuffer-python/commit/f52ac9ba6079b3a43952f9e5779d2b8089af9f63))

## 0.5.0-alpha.13 (2025-06-06)

Full Changelog: [v0.5.0-alpha.12...v0.5.0-alpha.13](https://github.com/turbopuffer/turbopuffer-python/compare/v0.5.0-alpha.12...v0.5.0-alpha.13)

### Features

* **api:** api update ([a016ffc](https://github.com/turbopuffer/turbopuffer-python/commit/a016ffc01f043eb8bd1b7061531966385e871461))
* **types:** add __setitem__ support to Row ([c2a4554](https://github.com/turbopuffer/turbopuffer-python/commit/c2a4554c7cd00e546ebd7a1447a42d6d863ec425))


### Bug Fixes

* **guide:** update UPGRADING.md ([c124d29](https://github.com/turbopuffer/turbopuffer-python/commit/c124d29ff94340c301e6e90ca294dda73bef9e7a))
* restore TYPE_CHECKING conditional in Row ([7d070a3](https://github.com/turbopuffer/turbopuffer-python/commit/7d070a38599511770269b82a3ce63ad9ce4dfb49))
* update supplemental codegen version ([1c68e54](https://github.com/turbopuffer/turbopuffer-python/commit/1c68e5414807fd5f0970b197e434c47ef8db123b))

## 0.5.0-alpha.12 (2025-06-03)

Full Changelog: [v0.5.0-alpha.11...v0.5.0-alpha.12](https://github.com/turbopuffer/turbopuffer-python/compare/v0.5.0-alpha.11...v0.5.0-alpha.12)

### Bug Fixes

* **types:** add missing fallback overloads for Row ([ca9c91f](https://github.com/turbopuffer/turbopuffer-python/commit/ca9c91fe2fe0d761f71a32d81d7a1b70ae2ad855))

## 0.5.0-alpha.11 (2025-06-03)

Full Changelog: [v0.5.0-alpha.10...v0.5.0-alpha.11](https://github.com/turbopuffer/turbopuffer-python/compare/v0.5.0-alpha.10...v0.5.0-alpha.11)

### Features

* **api:** api update ([14c2546](https://github.com/turbopuffer/turbopuffer-python/commit/14c25463edb34bd098eddc12f9f9cf49670b0845))
* **types:** add __setitem__ support to Row ([90a2a9a](https://github.com/turbopuffer/turbopuffer-python/commit/90a2a9a93ac921467ea3e175716361c346653643))

## 0.5.0-alpha.10 (2025-06-03)

Full Changelog: [v0.5.0-alpha.9...v0.5.0-alpha.10](https://github.com/turbopuffer/turbopuffer-python/compare/v0.5.0-alpha.9...v0.5.0-alpha.10)

### Features

* **api:** api update ([fe4083b](https://github.com/turbopuffer/turbopuffer-python/commit/fe4083b40d9bcfac42d5bb11017241d109d0f061))
* **client:** add follow_redirects request option ([051cc38](https://github.com/turbopuffer/turbopuffer-python/commit/051cc38792626bee8f9b69af013dc2fad25cb213))


### Bug Fixes

* **gen:** update to lastest API gen ([db879a2](https://github.com/turbopuffer/turbopuffer-python/commit/db879a261ce0778bde4cc4f29c4b3eb4020860c9))
* **guide:** add an upgrade guide ([5a9e1b0](https://github.com/turbopuffer/turbopuffer-python/commit/5a9e1b09d2fd1fd095b0aad602eccfcafb5990d6))
* **guide:** correct syntax in upgrade guide ([b7fec22](https://github.com/turbopuffer/turbopuffer-python/commit/b7fec22470472c7eaaf7d721b9632359e5c49eae))
* **tests:** update tests for new Row/Columns type names ([725c912](https://github.com/turbopuffer/turbopuffer-python/commit/725c9126d1f2d616852f42da5c18a2d30e26d52b))


### Chores

* **docs:** remove reference to rye shell ([038b2fd](https://github.com/turbopuffer/turbopuffer-python/commit/038b2fdae766bb3d6e230e232017516bf0970fe0))
* **docs:** remove unnecessary param examples ([c04f310](https://github.com/turbopuffer/turbopuffer-python/commit/c04f310879729b1f33a0be5c9daabc536a85daa7))

## 0.5.0-alpha.9 (2025-05-30)

Full Changelog: [v0.5.0-alpha.8...v0.5.0-alpha.9](https://github.com/turbopuffer/turbopuffer-python/compare/v0.5.0-alpha.8...v0.5.0-alpha.9)

### Bug Fixes

* **lib:** migrate utilities from turbopuffer_api into turbopuffer ([#103](https://github.com/turbopuffer/turbopuffer-python/issues/103)) ([a935a9f](https://github.com/turbopuffer/turbopuffer-python/commit/a935a9f361e4a23f566ecd0715fb522570c73727))

## 0.5.0-alpha.8 (2025-05-30)

Full Changelog: [v0.5.0-alpha.7...v0.5.0-alpha.8](https://github.com/turbopuffer/turbopuffer-python/compare/v0.5.0-alpha.7...v0.5.0-alpha.8)

### Features

* **api:** api update ([cea6680](https://github.com/turbopuffer/turbopuffer-python/commit/cea6680385db0d05f3b6a2d79177b237cc358092))

## 0.5.0-alpha.7 (2025-05-29)

Full Changelog: [v0.5.0-alpha.6...v0.5.0-alpha.7](https://github.com/turbopuffer/turbopuffer-python/compare/v0.5.0-alpha.6...v0.5.0-alpha.7)

### Features

* **api:** api update ([d9baa92](https://github.com/turbopuffer/turbopuffer-python/commit/d9baa92a98ed14ea11e27dbe087e4b38b5dbbaa4))
* **api:** api update ([c11242e](https://github.com/turbopuffer/turbopuffer-python/commit/c11242ec8b91de1c845bf08c5de7bb9d5e6d7248))
* **api:** api update ([f4eec91](https://github.com/turbopuffer/turbopuffer-python/commit/f4eec91b4af2d90bd270fab66854371e1e2c740b))
* **api:** api update ([99377d9](https://github.com/turbopuffer/turbopuffer-python/commit/99377d93e2583abe7342a0664b142dc49768fbea))
* **api:** api update ([aba8064](https://github.com/turbopuffer/turbopuffer-python/commit/aba8064540b05e5e4a870737a72ca568969fd733))

## 0.5.0-alpha.6 (2025-05-29)

Full Changelog: [v0.5.0-alpha.5...v0.5.0-alpha.6](https://github.com/turbopuffer/turbopuffer-python/compare/v0.5.0-alpha.5...v0.5.0-alpha.6)

### Features

* **api:** api update ([e0f19d6](https://github.com/turbopuffer/turbopuffer-python/commit/e0f19d62b77d44f0da244e837823993181e5288a))

## 0.5.0-alpha.5 (2025-05-29)

Full Changelog: [v0.5.0-alpha.4...v0.5.0-alpha.5](https://github.com/turbopuffer/turbopuffer-python/compare/v0.5.0-alpha.4...v0.5.0-alpha.5)

### Features

* **api:** api update ([f2f139e](https://github.com/turbopuffer/turbopuffer-python/commit/f2f139eea05eb309b23ba6a5c1c5a7ea0bffb1ac))
* **api:** api update ([a740c85](https://github.com/turbopuffer/turbopuffer-python/commit/a740c85537e1b5a00d605703cc2d71d220bc932f))

## 0.5.0-alpha.4 (2025-05-29)

Full Changelog: [v0.5.0-alpha.3...v0.5.0-alpha.4](https://github.com/turbopuffer/turbopuffer-python/compare/v0.5.0-alpha.3...v0.5.0-alpha.4)

### Features

* **api:** api update ([1a8824f](https://github.com/turbopuffer/turbopuffer-python/commit/1a8824fb229cb9a590ccdb9086ca3d4cc7436ee2))

## 0.5.0-alpha.3 (2025-05-29)

Full Changelog: [v0.5.0-alpha.2...v0.5.0-alpha.3](https://github.com/turbopuffer/turbopuffer-python/compare/v0.5.0-alpha.2...v0.5.0-alpha.3)

### Features

* **api:** api update ([f14461d](https://github.com/turbopuffer/turbopuffer-python/commit/f14461d883a929a979361677aa7f2f68bcf27ee2))
* **api:** api update ([77ebab5](https://github.com/turbopuffer/turbopuffer-python/commit/77ebab5faebc767fb9fa99e07536a2a7ad5a6552))
* **api:** api update ([0a13a70](https://github.com/turbopuffer/turbopuffer-python/commit/0a13a705a8a6715f03e4a716f869e78b359128d2))
* **api:** api update ([d486f26](https://github.com/turbopuffer/turbopuffer-python/commit/d486f26e59a7536d8fdeb98ddf150c2f5f9b1519))
* **api:** api update ([e3f1a7c](https://github.com/turbopuffer/turbopuffer-python/commit/e3f1a7cf8005e1d45621de41fc13314de53f285f))

## 0.5.0-alpha.2 (2025-05-29)

Full Changelog: [v0.5.0-alpha.1...v0.5.0-alpha.2](https://github.com/turbopuffer/turbopuffer-python/compare/v0.5.0-alpha.1...v0.5.0-alpha.2)

### Features

* **api:** api update ([c021d8b](https://github.com/turbopuffer/turbopuffer-python/commit/c021d8b89f5049e48c7b62c4543a887706b141fa))


### Bug Fixes

* **README:** add alpha notice ([14aac9d](https://github.com/turbopuffer/turbopuffer-python/commit/14aac9d3f1177316a90be10063248b2db70c38c3))
* **README:** update code examples ([12e9cca](https://github.com/turbopuffer/turbopuffer-python/commit/12e9ccada045c2a00c0bc8a5f4ab275c71bf9783))


### Chores

* remove custom code ([51c0514](https://github.com/turbopuffer/turbopuffer-python/commit/51c051481a85e719bfd97279bc2b8129e2c88d46))

## 0.5.0-alpha.1 (2025-05-28)

Full Changelog: [v0.4.0-alpha.1...v0.5.0-alpha.1](https://github.com/turbopuffer/turbopuffer-python/compare/v0.4.0-alpha.1...v0.5.0-alpha.1)

### Features

* **api:** api update ([a788c14](https://github.com/turbopuffer/turbopuffer-python/commit/a788c1422b699bd5c3e8179fa283e435d3bad099))
* **api:** api update ([6145878](https://github.com/turbopuffer/turbopuffer-python/commit/6145878ddb125fad92b686820824499aa194d569))
* **api:** api update ([ad14cdc](https://github.com/turbopuffer/turbopuffer-python/commit/ad14cdc0c77b47fde0b968364d83c856855c2976))
* **api:** api update ([dcbf9d6](https://github.com/turbopuffer/turbopuffer-python/commit/dcbf9d6002784d1050f76f80fe9005cfd2094117))
* **api:** api update ([d8352cf](https://github.com/turbopuffer/turbopuffer-python/commit/d8352cf2f0b597c8b1740f7227f484e8f3836e57))
* **api:** api update ([515404a](https://github.com/turbopuffer/turbopuffer-python/commit/515404abe1964666ffeeef986ef5faad3ebdb2c9))
* **api:** api update ([5e6045a](https://github.com/turbopuffer/turbopuffer-python/commit/5e6045a6eb1549da4f0d854ef3ed5c5077209057))
* **api:** api update ([a4869be](https://github.com/turbopuffer/turbopuffer-python/commit/a4869be8ead7fc0a1b155f7fac260c2a2add292a))
* **api:** api update ([cf67ed6](https://github.com/turbopuffer/turbopuffer-python/commit/cf67ed6bf343013f4d0aae4979dfb11fb87cd854))
* **api:** api update ([e3254ba](https://github.com/turbopuffer/turbopuffer-python/commit/e3254baf7458ac436d9c1b07336ff2a71de1538a))
* **api:** api update ([9c3feb5](https://github.com/turbopuffer/turbopuffer-python/commit/9c3feb5fa14cd0b2d0645f47789a36c966f6b357))
* **api:** api update ([419127d](https://github.com/turbopuffer/turbopuffer-python/commit/419127d3e2c75a899f4a021e03426f65b4c7a405))
* **api:** api update ([9849905](https://github.com/turbopuffer/turbopuffer-python/commit/98499056fcc525cbc3c3cef8b2c3a9154f325f24))
* **api:** api update ([594f35e](https://github.com/turbopuffer/turbopuffer-python/commit/594f35e7820c07144bebc83137d67501c133742c))
* **api:** api update ([74e8df3](https://github.com/turbopuffer/turbopuffer-python/commit/74e8df3f418919e4a6dcf25930cc44432cdceac1))
* **api:** api update ([a3a8330](https://github.com/turbopuffer/turbopuffer-python/commit/a3a833074a81d2dd09f30ae58bf2ed81de89d560))
* **api:** api update ([4bb390b](https://github.com/turbopuffer/turbopuffer-python/commit/4bb390b96bd6c243efc8d3c028349a14d7c210de))
* **api:** api update ([2b2412d](https://github.com/turbopuffer/turbopuffer-python/commit/2b2412dc78ed1e41c552ab1683b35ac7c19f0f07))
* **api:** api update ([73a5486](https://github.com/turbopuffer/turbopuffer-python/commit/73a5486f9c2752bf4310b3eefaec74ca40209142))
* **api:** api update ([f3ad602](https://github.com/turbopuffer/turbopuffer-python/commit/f3ad602c7b0fbc3164958db6693ccc036479a9c9))
* **api:** api update ([222504d](https://github.com/turbopuffer/turbopuffer-python/commit/222504d3c5d4654b4323aec6a26d49bb8e47923f))
* **api:** api update ([dd9d6c2](https://github.com/turbopuffer/turbopuffer-python/commit/dd9d6c2784d6490b9ac14e2999da3458f32b101a))
* **api:** api update ([20115c2](https://github.com/turbopuffer/turbopuffer-python/commit/20115c223f8c80c5735a354d6231e635d5bd6fb5))
* **api:** api update ([aa7bad5](https://github.com/turbopuffer/turbopuffer-python/commit/aa7bad5258a9a885a9105c4c59f48362de48ad8d))
* **api:** api update ([5a55074](https://github.com/turbopuffer/turbopuffer-python/commit/5a550741c22186dce371a24b9db8770c7ba774f3))
* **api:** api update ([eb5afb2](https://github.com/turbopuffer/turbopuffer-python/commit/eb5afb2d63afb4e7db4a7cd22506aa2f953e9c6e))
* **api:** api update ([1a4ce60](https://github.com/turbopuffer/turbopuffer-python/commit/1a4ce60b7ed12aea579e9dbfcec07b866c82d405))
* **api:** api update ([27c0374](https://github.com/turbopuffer/turbopuffer-python/commit/27c0374a230a1437c6b6cda9c218e661575ddc23))
* **api:** api update ([49acdc2](https://github.com/turbopuffer/turbopuffer-python/commit/49acdc26db850f8a86c376e0f19b793ef801088a))
* **api:** api update ([9d26749](https://github.com/turbopuffer/turbopuffer-python/commit/9d26749c2424e1a880825095505b8e17e04037f9))
* **api:** api update ([5b5e258](https://github.com/turbopuffer/turbopuffer-python/commit/5b5e258cb1fb4b54e1d3498c4672fdf9a27e681a))
* **api:** api update ([f119560](https://github.com/turbopuffer/turbopuffer-python/commit/f119560317d9858b7b5ed7274298464861c29cbb))
* **api:** api update ([b40a258](https://github.com/turbopuffer/turbopuffer-python/commit/b40a2580b2d481f5837f8aeb2cb03d749249873c))
* **api:** api update ([de09eb6](https://github.com/turbopuffer/turbopuffer-python/commit/de09eb6c87117a2d8927e5f53b4655c8be00c6e2))
* **api:** api update ([e5b907b](https://github.com/turbopuffer/turbopuffer-python/commit/e5b907be45c71cf42a5ef4f6304522fc665abe90))
* **api:** api update ([82c07a0](https://github.com/turbopuffer/turbopuffer-python/commit/82c07a0ea9e122d3636e39f80ef56ada5ba25d32))
* **api:** api update ([4aff84f](https://github.com/turbopuffer/turbopuffer-python/commit/4aff84ff7fff1ace200c2b30556b5545a6c58a06))
* **api:** manual updates ([01965c9](https://github.com/turbopuffer/turbopuffer-python/commit/01965c91651b1281351c081931febe8a08366aa6))


### Chores

* **ci:** fix installation instructions ([b2dbc95](https://github.com/turbopuffer/turbopuffer-python/commit/b2dbc95e8673f2bae76415146d44b9f6c5e3c618))
* **ci:** upload sdks to package manager ([75e82da](https://github.com/turbopuffer/turbopuffer-python/commit/75e82da8841da9bc4b1a95ed217d36c01c7c0aeb))
* **docs:** grammar improvements ([7ccc03b](https://github.com/turbopuffer/turbopuffer-python/commit/7ccc03b63bd7e8b7ae6f8bf9ce9e763ca417129d))
* **internal:** codegen related update ([69a757e](https://github.com/turbopuffer/turbopuffer-python/commit/69a757e26d67c9a4ccdbb404139322305e21884b))
* **internal:** version bump ([00aa607](https://github.com/turbopuffer/turbopuffer-python/commit/00aa607c35dd4084db6cd10da399d73010280367))

## 0.4.0-alpha.1 (2025-05-13)

Full Changelog: [v0.3.0...v0.4.0-alpha.1](https://github.com/turbopuffer/turbopuffer-python/compare/v0.3.0...v0.4.0-alpha.1)

### Features

* **api:** api update ([bdfdccc](https://github.com/turbopuffer/turbopuffer-python/commit/bdfdcccf5df28cd5104999e14eddb5d175c644b7))


### Chores

* sync repo ([2fcc00d](https://github.com/turbopuffer/turbopuffer-python/commit/2fcc00d3785df736721933c43cf2cf5693027ca5))
* update SDK settings ([1f814f3](https://github.com/turbopuffer/turbopuffer-python/commit/1f814f39dcd7dfe4838fc0e9aa42a966ad44f28f))
* update SDK settings ([513b09d](https://github.com/turbopuffer/turbopuffer-python/commit/513b09dc2ae33fe633690ca2f92b1a972dbf5560))
