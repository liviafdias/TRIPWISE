(ns api.coreapi
  (:require [clj-http.client :as client]
            [cheshire.core :as json]
            [ring.adapter.jetty :refer [run-jetty]]))

;; API Configuration
(def api-key "4879c51b145b63c6355d0521af04c4be") ;; Insira sua chave da Odds API aqui
(def base-url "https://api.the-odds-api.com/v4/sports")

;; State Management
(def accounts (atom {})) ;; {user-id {:balance 0.0 :bets []}}

;; Utility functions for Odds API
(defn fetch-sports []
  (let [url (str base-url "?apiKey=" api-key)]
    (-> (client/get url {:as :json})
        :body)))

(defn fetch-odds [sport]
  (let [url (str base-url "/" sport "/odds?apiKey=" api-key "&regions=us&markets=h2h,spreads,totals")]
    (-> (client/get url {:as :json})
        :body)))

;; Account management
(defn deposit [user-id amount]
  (swap! accounts update-in [user-id :balance] (fnil + 0) amount))

(defn get-balance [user-id]
  (get-in @accounts [user-id :balance] 0))

(defn register-bet [user-id bet]
  (swap! accounts update-in [user-id :bets] conj bet))

(defn get-bets [user-id]
  (get-in @accounts [user-id :bets] []))

;; Web server with Ring
(defn handle-request [request]
  (let [{:keys [uri method query-params]} request
        user-id (get query-params "user-id")]
    (case [method uri]
      ;; Deposit endpoint
      [:post "/deposit"]
      (let [amount (Double/parseDouble (get query-params "amount" "0"))]
        (deposit user-id amount)
        {:status 200 :body (str "Deposited " amount " to user " user-id)})

      ;; Get Balance
      [:get "/balance"]
      {:status 200 :body (str "Balance for user " user-id ": " (get-balance user-id))}

      ;; Fetch Sports
      [:get "/sports"]
      {:status 200 :body (json/generate-string (fetch-sports))}

      ;; Fetch Odds for a Sport
      [:get "/odds"]
      (let [sport (get query-params "sport")]
        {:status 200 :body (json/generate-string (fetch-odds sport))})

      ;; Register Bet
      [:post "/bet"]
      (let [bet (json/parse-string (get query-params "bet") true)]
        (register-bet user-id bet)
        {:status 200 :body "Bet registered successfully"})

      ;; Get Bets
      [:get "/bets"]
      {:status 200 :body (json/generate-string (get-bets user-id))}

      ;; Default case
      {:status 404 :body "Endpoint not found"})))

(defn start-server []
  (run-jetty handle-request {:port 3000 :join? false}))

;; Start server
(start-server)