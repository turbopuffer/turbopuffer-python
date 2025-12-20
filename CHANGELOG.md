# Changelog

## 1.12.0 (2025-12-20)

Full Changelog: [v1.11.0...v1.12.0](https://github.com/turbopuffer/turbopuffer-python/compare/v1.11.0...v1.12.0)

### Features

* remove compatibility shims ([#196](https://github.com/turbopuffer/turbopuffer-python/issues/196)) ([fde7344](https://github.com/turbopuffer/turbopuffer-python/commit/fde7344ad9962cdb7c77d444e01c0ebbcd193915))


### Bug Fixes

* use async_to_httpx_files in patch method ([19d2b70](https://github.com/turbopuffer/turbopuffer-python/commit/19d2b70db29f232da9f489b5b83b1d43dae62f94))


### Chores

* **internal:** codegen related update ([76f6c01](https://github.com/turbopuffer/turbopuffer-python/commit/76f6c012dc2e11e6d6c85b1b7fdd2133fb79a34c))
* speedup initial import ([f98097d](https://github.com/turbopuffer/turbopuffer-python/commit/f98097de4d399b4c7e19b1234820eae12e880ba8))

## 1.11.0 (2025-12-15)

Full Changelog: [v1.10.0...v1.11.0](https://github.com/turbopuffer/turbopuffer-python/compare/v1.10.0...v1.11.0)

### Features

* add word_v3 to the spec ([634b7f2](https://github.com/turbopuffer/turbopuffer-python/commit/634b7f272e71bfabda310649d136f613bae83ed1))


### Bug Fixes

* **types:** allow pyright to infer TypedDict types within SequenceNotStr ([2c2a4bc](https://github.com/turbopuffer/turbopuffer-python/commit/2c2a4bc039d797b11981d1da388fd2cc5e31f78b))


### Chores

* add missing docstrings ([1f04083](https://github.com/turbopuffer/turbopuffer-python/commit/1f04083d328be8f1f1805bfc55bd044ee2e56324))
* **internal:** add missing files argument to base client ([7afed9a](https://github.com/turbopuffer/turbopuffer-python/commit/7afed9a2bbc1184ce28430316035383cf248ee8f))

## 1.10.0 (2025-12-06)

Full Changelog: [v1.9.1...v1.10.0](https://github.com/turbopuffer/turbopuffer-python/compare/v1.9.1...v1.10.0)

### Features

* always install orjson, even without the [fast] extra ([#192](https://github.com/turbopuffer/turbopuffer-python/issues/192)) ([06a1420](https://github.com/turbopuffer/turbopuffer-python/commit/06a1420645f551ec9e22a931d0ff69dff2dd6814))
* disable compression by default ([#190](https://github.com/turbopuffer/turbopuffer-python/issues/190)) ([34c1e32](https://github.com/turbopuffer/turbopuffer-python/commit/34c1e32989df97fa9baf25b079a8c3d7a8d1ddae))

## 1.9.1 (2025-12-05)

Full Changelog: [v1.9.0...v1.9.1](https://github.com/turbopuffer/turbopuffer-python/compare/v1.9.0...v1.9.1)

## 1.9.0 (2025-12-05)

Full Changelog: [v1.9.0-beta.4...v1.9.0](https://github.com/turbopuffer/turbopuffer-python/compare/v1.9.0-beta.4...v1.9.0)

### Chores

* codegen updates ([df997d6](https://github.com/turbopuffer/turbopuffer-python/commit/df997d67516e1193239247f3794dc4fcf6812df4))

## 1.9.0-beta.4 (2025-12-04)

Full Changelog: [v1.9.0-beta.3...v1.9.0-beta.4](https://github.com/turbopuffer/turbopuffer-python/compare/v1.9.0-beta.3...v1.9.0-beta.4)

## 1.9.0-beta.3 (2025-12-02)

Full Changelog: [v1.9.0-beta.2...v1.9.0-beta.3](https://github.com/turbopuffer/turbopuffer-python/compare/v1.9.0-beta.2...v1.9.0-beta.3)

### Features

* sdks: add &lt;patch|delete&gt;_by_filter_allow_partial options ([ffac88a](https://github.com/turbopuffer/turbopuffer-python/commit/ffac88af0fb787776ed96076c892e4d70b8fd85d))


### Chores

* **docs:** use environment variables for authentication in code snippets ([26df7ea](https://github.com/turbopuffer/turbopuffer-python/commit/26df7ea743c81e4e66ef1ebe72d32ef91ac29f79))
* update lockfile ([679604c](https://github.com/turbopuffer/turbopuffer-python/commit/679604c9a2fafe668fdebbf482514dd9d7362955))


### Documentation

* add cross-region copy_from_namespace to write API docs ([749b349](https://github.com/turbopuffer/turbopuffer-python/commit/749b349674e317d0af41461b5c55d17e70265248))

## 1.9.0-beta.2 (2025-12-02)

Full Changelog: [v1.9.0-beta.1...v1.9.0-beta.2](https://github.com/turbopuffer/turbopuffer-python/compare/v1.9.0-beta.1...v1.9.0-beta.2)

## 1.9.0-beta.1 (2025-12-02)

Full Changelog: [v1.8.1...v1.9.0-beta.1](https://github.com/turbopuffer/turbopuffer-python/compare/v1.8.1...v1.9.0-beta.1)

### Performance Improvements

* skip unneeded transformations for primitive types and tuples ([#178](https://github.com/turbopuffer/turbopuffer-python/issues/178)) ([8dbed44](https://github.com/turbopuffer/turbopuffer-python/commit/8dbed446745e90dc010e56cc6e47ffcb719fd094))

## 1.8.1 (2025-12-01)

Full Changelog: [v1.8.0...v1.8.1](https://github.com/turbopuffer/turbopuffer-python/compare/v1.8.0...v1.8.1)

### Bug Fixes

* ensure streams are always closed ([91cb8d5](https://github.com/turbopuffer/turbopuffer-python/commit/91cb8d54dd7804c88c5b9c1c659a806c0d664fd0))
* **tests:** use BM25 query with distinct scores ([#179](https://github.com/turbopuffer/turbopuffer-python/issues/179)) ([508994e](https://github.com/turbopuffer/turbopuffer-python/commit/508994e52f0e5ef3ddf347a3f4fd22dc0f855531))


### Chores

* **deps:** mypy 1.18.1 has a regression, pin to 1.17 ([8cebf8f](https://github.com/turbopuffer/turbopuffer-python/commit/8cebf8f09dea0252da7570c08bb924fb5fcb3587))

## 1.8.0 (2025-11-25)

Full Changelog: [v1.7.0...v1.8.0](https://github.com/turbopuffer/turbopuffer-python/compare/v1.7.0...v1.8.0)

### Features

* site: add ascii_folding to docs and SDKs ([7be788c](https://github.com/turbopuffer/turbopuffer-python/commit/7be788cb25ccac18a21ef05dec58c3e9556c3adb))


### Chores

* **internal:** codegen related update ([93ebd24](https://github.com/turbopuffer/turbopuffer-python/commit/93ebd246fd667d3393733b0e531c297b3ba80b01))

## 1.7.0 (2025-11-17)

Full Changelog: [v1.6.0...v1.7.0](https://github.com/turbopuffer/turbopuffer-python/compare/v1.6.0...v1.7.0)

### Features

* spec: add support for cross-org CFN to SDKs ([8d4cb17](https://github.com/turbopuffer/turbopuffer-python/commit/8d4cb17108cf5f14af4aee321b656ad5a0fbfece))

## 1.6.0 (2025-11-17)

Full Changelog: [v1.5.0...v1.6.0](https://github.com/turbopuffer/turbopuffer-python/compare/v1.5.0...v1.6.0)

### Features

* Add vector attribute schema to metadata endpoint ([0d4d216](https://github.com/turbopuffer/turbopuffer-python/commit/0d4d2169a7048f20308490b17fa4cbc184f85112))
* Allow for a CMEK key to be specified in copy_from_namespace ([2e85faa](https://github.com/turbopuffer/turbopuffer-python/commit/2e85faa4b5cacfbd3b840ed80c3d8c528e2aeff9))
* Make `type` required on `AttributeSchemaConfig` ([677d239](https://github.com/turbopuffer/turbopuffer-python/commit/677d2390c9640bbf80eb74ad258e9b9ea7a5e9dd))
* openapi: Fix stainless warnings ([b12a54b](https://github.com/turbopuffer/turbopuffer-python/commit/b12a54b9b9062be3efca3618c2a9cbbbfc3e7ef2))
* openapi: name variants of `NamespaceMetadata.index` ([ddc8d26](https://github.com/turbopuffer/turbopuffer-python/commit/ddc8d268b08466967e3134c1cd2995e52d4efb46))


### Bug Fixes

* **client:** close streams without requiring full consumption ([b8d32f3](https://github.com/turbopuffer/turbopuffer-python/commit/b8d32f3d1af9fd7052bc0ea52c8446ae4ea3a61b))
* compat with Python 3.14 ([67195f2](https://github.com/turbopuffer/turbopuffer-python/commit/67195f2f74449cc4e50d494d46bdbb736e3f8375))
* **compat:** update signatures of `model_dump` and `model_dump_json` for Pydantic v1 ([595f416](https://github.com/turbopuffer/turbopuffer-python/commit/595f416c6d8d1362fb2108444af9d41fae8eb6e5))


### Chores

* **internal/tests:** avoid race condition with implicit client cleanup ([4230de9](https://github.com/turbopuffer/turbopuffer-python/commit/4230de956fb48b58753bef7dccfc271d6f9111c2))
* **internal/tests:** avoid race condition with implicit client cleanup ([1386b25](https://github.com/turbopuffer/turbopuffer-python/commit/1386b251b944769f4023e2c2cf6f589e05fa1db7))
* **internal:** grammar fix (it's -&gt; its) ([7620a5a](https://github.com/turbopuffer/turbopuffer-python/commit/7620a5a61739540fe0fa528a643e6921cf415148))
* **package:** drop Python 3.8 support ([b0a801e](https://github.com/turbopuffer/turbopuffer-python/commit/b0a801e514f06a672dd575aaf00d8ea0935582a4))

## 1.5.0 (2025-10-21)

Full Changelog: [v1.4.1...v1.5.0](https://github.com/turbopuffer/turbopuffer-python/compare/v1.4.1...v1.5.0)

### Features

* Metadata endpoint updates (e.g. to track indexing progress) ([03baa87](https://github.com/turbopuffer/turbopuffer-python/commit/03baa8777f150cae9f8f4f0342d50b57d67dc96f))
* required for patch_by_filter :facepalm: ([fd6692f](https://github.com/turbopuffer/turbopuffer-python/commit/fd6692fe39ebc331c096df48dfb2f8def6dc991b))
* stainless: add patch_by_filter ([e097f85](https://github.com/turbopuffer/turbopuffer-python/commit/e097f856064715c1010e26a1b8969596bb1870ae))


### Chores

* bump `httpx-aiohttp` version to 0.1.9 ([eba6dd4](https://github.com/turbopuffer/turbopuffer-python/commit/eba6dd41e90bc0994248e260bc3052d876a7438f))
* Correct python types for patch by filter (and conditional writes) ([#172](https://github.com/turbopuffer/turbopuffer-python/issues/172)) ([fb3257e](https://github.com/turbopuffer/turbopuffer-python/commit/fb3257e98d0fed3fe64385acbafd0c19ba191600))

## 1.4.1 (2025-10-15)

Full Changelog: [v1.4.0...v1.4.1](https://github.com/turbopuffer/turbopuffer-python/compare/v1.4.0...v1.4.1)

## 1.4.0 (2025-10-15)

Full Changelog: [v1.3.1...v1.4.0](https://github.com/turbopuffer/turbopuffer-python/compare/v1.3.1...v1.4.0)

### Features

* Add float, []float and []bool to the list of valid types in the OpenAPI spec. ([11b13d8](https://github.com/turbopuffer/turbopuffer-python/commit/11b13d8b27d5af4bc01c52bbf53cbf6e313a110b))
* Promote disable_backpressure to first-class Write property ([adf659a](https://github.com/turbopuffer/turbopuffer-python/commit/adf659ad1c9a45180d6c18531ded370fa433bed4))


### Chores

* **internal:** detect missing future annotations with ruff ([6e631de](https://github.com/turbopuffer/turbopuffer-python/commit/6e631de8f0af1da81f15b9890cb49b1adcedfcde))

## 1.3.1 (2025-10-06)

Full Changelog: [v1.3.0...v1.3.1](https://github.com/turbopuffer/turbopuffer-python/compare/v1.3.0...v1.3.1)

### Documentation

* hint_cache_warm also update header and openapi ([2088d85](https://github.com/turbopuffer/turbopuffer-python/commit/2088d8564c13541a52887bb872194527dfc2eede))

## 1.3.0 (2025-09-24)

Full Changelog: [v1.2.0...v1.3.0](https://github.com/turbopuffer/turbopuffer-python/compare/v1.2.0...v1.3.0)

### Features

* add WithParams variant to BM25 and ContainsAllTokens ([cef6f72](https://github.com/turbopuffer/turbopuffer-python/commit/cef6f72c519212528135565fcea2ac1fe169c519))


### Bug Fixes

* **compat:** compat with `pydantic&lt;2.8.0` when using additional fields ([1268479](https://github.com/turbopuffer/turbopuffer-python/commit/126847904b5739e5c6ef4803846fd0e7567a485d))


### Chores

* do not install brew dependencies in ./scripts/bootstrap by default ([024c0a4](https://github.com/turbopuffer/turbopuffer-python/commit/024c0a4d72851696b058df1d5f76fb7798cf9288))
* **internal:** update pydantic dependency ([067d75e](https://github.com/turbopuffer/turbopuffer-python/commit/067d75ec42a305be9f9d5b03424c0486825289b4))
* **types:** change optional parameter type from NotGiven to Omit ([8d6c3cb](https://github.com/turbopuffer/turbopuffer-python/commit/8d6c3cb1ad8e34e3f01e93b31e569536ee8d49e6))

## 1.2.0 (2025-09-11)

Full Changelog: [v1.1.0...v1.2.0](https://github.com/turbopuffer/turbopuffer-python/compare/v1.1.0...v1.2.0)

### Features

* improve future compat with pydantic v3 ([819a5d1](https://github.com/turbopuffer/turbopuffer-python/commit/819a5d154c7352ea4e85b99775529d074aad73f7))
* spec: add dedicated type for AggregationGroup response ([c8bc23f](https://github.com/turbopuffer/turbopuffer-python/commit/c8bc23f80212ce8d4923af09160c542d5e0b609d))
* tpuf: add include_ground_truth option to recall endpoint ([2128270](https://github.com/turbopuffer/turbopuffer-python/commit/21282704752e68f67fa784d8c89edc0a4e8b6056))


### Chores

* **internal:** codegen related update ([5c8f96b](https://github.com/turbopuffer/turbopuffer-python/commit/5c8f96bcab380f3cc6c10b6faced0b30bcf3fdd1))
* **internal:** move mypy configurations to `pyproject.toml` file ([f72115d](https://github.com/turbopuffer/turbopuffer-python/commit/f72115da5c839670e24798693998afef60f3a038))

## 1.1.0 (2025-09-02)

Full Changelog: [v1.0.0...v1.1.0](https://github.com/turbopuffer/turbopuffer-python/compare/v1.0.0...v1.1.0)

### Features

* **types:** replace List[str] with SequenceNotStr in params ([212f234](https://github.com/turbopuffer/turbopuffer-python/commit/212f234b09822f7fd315cff43c6f7676ab2202c0))


### Chores

* **internal:** add Sequence related utils ([f5b1d00](https://github.com/turbopuffer/turbopuffer-python/commit/f5b1d001ed91192de5082feb7058d2150e73a1d8))

## 1.0.0 (2025-08-28)

Full Changelog: [v0.6.5...v1.0.0](https://github.com/turbopuffer/turbopuffer-python/compare/v0.6.5...v1.0.0)

### Features

* Make word_v2 the default FTS tokenizer ([4b566d7](https://github.com/turbopuffer/turbopuffer-python/commit/4b566d752773bd7216dd5183fda8f4284be9e36e))


### Bug Fixes

* avoid newer type syntax ([a5fb4a6](https://github.com/turbopuffer/turbopuffer-python/commit/a5fb4a6c546d712aafe395ff281c67d5f9a2591c))


### Chores

* **internal:** change ci workflow machines ([eaed93c](https://github.com/turbopuffer/turbopuffer-python/commit/eaed93c8b03d03ace9c417551141ddc6ef45bca7))
* **internal:** update pyright exclude list ([b7ad4ef](https://github.com/turbopuffer/turbopuffer-python/commit/b7ad4ef6b40eab65f7a66fb6bee8f9e935808369))
* update github action ([9fe3df7](https://github.com/turbopuffer/turbopuffer-python/commit/9fe3df78346c03091da5c793980f40a68c9e8c8c))

## 0.6.5 (2025-08-18)

Full Changelog: [v0.6.4...v0.6.5](https://github.com/turbopuffer/turbopuffer-python/compare/v0.6.4...v0.6.5)

### Bug Fixes

* **api:** add support for `group_by` query parameter ([c809351](https://github.com/turbopuffer/turbopuffer-python/commit/c8093514e1bd5ce169ab594f4e532b7e4deae7b6))

## 0.6.4 (2025-08-13)

Full Changelog: [v0.6.3...v0.6.4](https://github.com/turbopuffer/turbopuffer-python/compare/v0.6.3...v0.6.4)

## 0.6.3 (2025-08-12)

Full Changelog: [v0.6.2...v0.6.3](https://github.com/turbopuffer/turbopuffer-python/compare/v0.6.2...v0.6.3)

### Bug Fixes

* remove 200 error code for hint_cache_warm API call (always 202 now) ([77df5be](https://github.com/turbopuffer/turbopuffer-python/commit/77df5be5bddbff03429ccff6cd316145a0a5e90e))


### Chores

* **internal:** codegen related update ([b4c305d](https://github.com/turbopuffer/turbopuffer-python/commit/b4c305d444cd4958a85774ecb2a7d07b583b670c))

## 0.6.2 (2025-08-11)

Full Changelog: [v0.6.1...v0.6.2](https://github.com/turbopuffer/turbopuffer-python/compare/v0.6.1...v0.6.2)

### Chores

* **internal:** update comment in script ([368d5dd](https://github.com/turbopuffer/turbopuffer-python/commit/368d5dd1e766e7890aee6b89d52560291911571f))
* update @stainless-api/prism-cli to v5.15.0 ([38948fa](https://github.com/turbopuffer/turbopuffer-python/commit/38948fabee3a13a5008957fe92499d767949d249))

## 0.6.1 (2025-08-08)

Full Changelog: [v0.6.0...v0.6.1](https://github.com/turbopuffer/turbopuffer-python/compare/v0.6.0...v0.6.1)

### Bug Fixes

* use strict types for explain_query ([#148](https://github.com/turbopuffer/turbopuffer-python/issues/148)) ([7c3bff1](https://github.com/turbopuffer/turbopuffer-python/commit/7c3bff1fd7ac3dd1bb60ba0dd983314d61eef95e))


### Chores

* **internal:** fix ruff target version ([3e5ec06](https://github.com/turbopuffer/turbopuffer-python/commit/3e5ec067bb06d0f4e6c9b72aeb483362a4f050d9))

## 0.6.0 (2025-07-31)

Full Changelog: [v0.5.17...v0.6.0](https://github.com/turbopuffer/turbopuffer-python/compare/v0.5.17...v0.6.0)

### Features

* **client:** support file upload requests ([ffdbc5d](https://github.com/turbopuffer/turbopuffer-python/commit/ffdbc5d585b348a39551c016ba1d8afc77687fa4))


### Bug Fixes

* **api:** api update ([18eee10](https://github.com/turbopuffer/turbopuffer-python/commit/18eee10603b4113034623568f927d9ab5295f6b2))
* **api:** api update ([dcf8fd1](https://github.com/turbopuffer/turbopuffer-python/commit/dcf8fd16ab08f2d238ec578015e25a48b8852ded))

## 0.5.17 (2025-07-29)

Full Changelog: [v0.5.16...v0.5.17](https://github.com/turbopuffer/turbopuffer-python/compare/v0.5.16...v0.5.17)

### Bug Fixes

* **api:** api update ([47fbda1](https://github.com/turbopuffer/turbopuffer-python/commit/47fbda100c87aacb8962ce3b0a589ca787d48ecf))
* **api:** api update ([c8a3a2f](https://github.com/turbopuffer/turbopuffer-python/commit/c8a3a2f5b028ff92e8c17ca52b86a35d3ae1e6eb))
* **api:** api update ([882c8b4](https://github.com/turbopuffer/turbopuffer-python/commit/882c8b4a992a78c2057db3021ea84e1a85e465b6))

## 0.5.16 (2025-07-29)

Full Changelog: [v0.5.15...v0.5.16](https://github.com/turbopuffer/turbopuffer-python/compare/v0.5.15...v0.5.16)

### Bug Fixes

* add support for regex filter ([6fb42f9](https://github.com/turbopuffer/turbopuffer-python/commit/6fb42f9cc98ada3def222c9ca1b639ffe10f1434))
* **api:** api update ([12a8eb6](https://github.com/turbopuffer/turbopuffer-python/commit/12a8eb6e068bf23a3df3553df2d20c9f87caffb0))
* **api:** api update ([c84043a](https://github.com/turbopuffer/turbopuffer-python/commit/c84043a92c31555a0d1f7c7f320d0a1ad7147261))
* **api:** api update ([8eeaf90](https://github.com/turbopuffer/turbopuffer-python/commit/8eeaf90624de0d7aafca55cb139ba2651838cfc2))

## 0.5.15 (2025-07-28)

Full Changelog: [v0.5.14...v0.5.15](https://github.com/turbopuffer/turbopuffer-python/compare/v0.5.14...v0.5.15)

### Bug Fixes

* **api:** api update ([ed06b6f](https://github.com/turbopuffer/turbopuffer-python/commit/ed06b6f1aa3d72dd3e6b3a4317dbe326b0b8ee7c))
* more precise types for filters that take arrays ([3f8a227](https://github.com/turbopuffer/turbopuffer-python/commit/3f8a2272b3ea062468dd8454f157c2295fc32e37))
* serialize datetime objects when orjson isn't installed ([#143](https://github.com/turbopuffer/turbopuffer-python/issues/143)) ([c194fc6](https://github.com/turbopuffer/turbopuffer-python/commit/c194fc6bae0cf1ab0696fa98736de78ef99a536a))


### Chores

* **project:** add settings file for vscode ([c843ee0](https://github.com/turbopuffer/turbopuffer-python/commit/c843ee0a0e91b50b97222fef804aa464de841903))

## 0.5.14 (2025-07-22)

Full Changelog: [v0.5.13...v0.5.14](https://github.com/turbopuffer/turbopuffer-python/compare/v0.5.13...v0.5.14)

### Bug Fixes

* **parsing:** ignore empty metadata ([1c750c2](https://github.com/turbopuffer/turbopuffer-python/commit/1c750c228f2b028355d402a5085c3ddadc9bb749))
* **parsing:** parse extra field types ([fc021b2](https://github.com/turbopuffer/turbopuffer-python/commit/fc021b2c8f046e00055ea8b7ac302c2708a47cf3))

## 0.5.13 (2025-07-18)

Full Changelog: [v0.5.12...v0.5.13](https://github.com/turbopuffer/turbopuffer-python/compare/v0.5.12...v0.5.13)

### Features

* clean up environment call outs ([f0c7314](https://github.com/turbopuffer/turbopuffer-python/commit/f0c73145365f897255517af9f4d417bb064886e2))


### Bug Fixes

* **client:** don't send Content-Type header on GET requests ([534cd40](https://github.com/turbopuffer/turbopuffer-python/commit/534cd40ef0af133f854f5336dcf16922fa08332a))


### Chores

* **readme:** fix version rendering on pypi ([341d3a3](https://github.com/turbopuffer/turbopuffer-python/commit/341d3a332a8b18886c7de9ac606d63258142ecc4))

## 0.5.12 (2025-07-10)

Full Changelog: [v0.5.11...v0.5.12](https://github.com/turbopuffer/turbopuffer-python/compare/v0.5.11...v0.5.12)

### Bug Fixes

* **api:** api update ([b49220a](https://github.com/turbopuffer/turbopuffer-python/commit/b49220a2fa8b88a107ea8f0fbb20671bd29266fe))
* **api:** api update ([1a49cae](https://github.com/turbopuffer/turbopuffer-python/commit/1a49caec78bbc71c1678bbc4b89b8d3017269c6b))
* don't set region in tests if base URL doesn't support it ([b7e8297](https://github.com/turbopuffer/turbopuffer-python/commit/b7e8297f705be97edee77f41487c51ae7bc975cb))
* explicitly omit TURBOPUFFER_BASE_URL from env when necessary ([9075015](https://github.com/turbopuffer/turbopuffer-python/commit/9075015991d9afa886d31a327a55959699aaeda7))
* **parsing:** correctly handle nested discriminated unions ([7c63c5e](https://github.com/turbopuffer/turbopuffer-python/commit/7c63c5e93af2e7615ea0eb10f40e28926ac319f3))
* update tests for new metadata endpoint ([a6799d3](https://github.com/turbopuffer/turbopuffer-python/commit/a6799d30683595281cfd14dfff014cc1725407d0))

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
