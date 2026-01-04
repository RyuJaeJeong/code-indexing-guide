## Javascript 프로젝트 파싱
 
```cmd
npm install -g @sourcegraph/scip-typescript
scip-typescript index --infer-tsconfig
```
필요시 프로젝트 루트 경로에 tsconfig.json 추가 할 것 
```json
{
  "compilerOptions": {
    "target": "esnext",
    "module": "commonjs",
    "lib": ["esnext", "dom"],
    "allowJs": true,           
    "checkJs": false,          
    "jsx": "preserve",         
    "noEmit": true,            
    "skipLibCheck": true
  },
  "include": [
    "src/**/*",
    "pages/**/*",
    "app/**/*",
    "components/**/*",
    "lib/**/*",
    "utils/**/*",
    "*.js",
    "*.jsx"
  ],
  "exclude": [
    "node_modules",
    ".next",
    "out"
  ]
}
```
필요시 검토할 것 
>To improve the quality of indexing results for JavaScript, consider adding @types/* packages as devDependencies in package.json.