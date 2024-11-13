(defproject sports-betting "0.1.0-SNAPSHOT"
  :description "FIXME: write description"
  :url "http://example.com/FIXME"
  :license {:name "Eclipse Public License"
            :url "http://www.eclipse.org/legal/epl-v10.html"}
  :dependencies [[org.clojure/clojure "1.10.0"]
                 [org.clojure/tools.cli "0.4.1"] ;; inclusão da biblioteca para interpretação de argumentos
                 [clj-http "3.9.1"] ;; inclusão da biblioteca para requisições HTTP 
                 [cheshire "5.8.1"]  ;; inclusão da biblioteca para manipular JSON
                 [ring/ring-core "1.7.1"]
                 [ring/ring-jetty-adapter "1.7.1"]]
  :main ^:skip-aot sports-betting.core
  ;;:main sports-betting.core
  :target-path "target/%s"
  :profiles {:uberjar {:aot :all
                       :jvm-opts ["-Dclojure.compiler.direct-linking=true"]}})
