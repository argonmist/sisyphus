Feature: 使用者登入

  Scenario: 忘記密碼
    Given 使用者已有PGTalk帳號密碼且為登出狀態
    When 忘記密碼頁輸入資訊並取得手機驗證碼
    Then 可取回密碼
    Then 可用新密碼登入PGTalk

