// /system/modules/zoya.consent/resources/js/klaro-config.js
var klaroConfig = {
  version: 6,
  elementID: 'klaro',
  storageMethod: 'cookie',
  cookieName: 'ol-consent',
  cookieExpiresAfterDays: 180,
  cookieDomain: null,

  mustConsent: false,
  default: false,
  acceptAll: true,
  hideDeclineAll: false,
  hideLearnMore: false,
  groupByPurpose: true,
  testing: true, // برای تست: بنر همیشه نشان داده می‌شود

  purposes: [
    'essential',
    'security',
    'analytics',
    'external',
    'support',
    'payments',
    'personalization'
  ],

  apps: [
    { name: 'essential-cookies', title: 'Essential cookies', purposes: ['essential'], required: true, optOut: false,
      cookies: ['JSESSIONID','opencms_session','ocLocale','ocEdit*'] },

    // یکی از این دو را اگر داری نگه دار:
    { name: 'recaptcha',  title: 'Google reCAPTCHA',        purposes: ['security'] },
    { name: 'turnstile',  title: 'Cloudflare Turnstile',    purposes: ['security'] },

    // یکی را انتخاب کن (GA4 یا Matomo):
    { name: 'ga4',    title: 'Google Analytics 4', purposes: ['analytics'], cookies: [/^_ga/, /^_gid/, /^_gat/] },
    { name: 'matomo', title: 'Matomo',             purposes: ['analytics'], cookies: [/^_pk_/, /^_pk_s/] },

    // رسانه/نقشه
    { name: 'youtube', title: 'YouTube embeds', purposes: ['external'], contextualConsentOnly: true, cookies: ['VISITOR_INFO1_LIVE','YSC'] },
    { name: 'vimeo',   title: 'Vimeo embeds',   purposes: ['external'], contextualConsentOnly: true, cookies: ['vuid'] },
    { name: 'gmap',    title: 'Google Maps',    purposes: ['external'], contextualConsentOnly: true },

    // پشتیبانی
    { name: 'tawkto',   title: 'Tawk.to (live chat)', purposes: ['support'] },
    { name: 'intercom', title: 'Intercom',           purposes: ['support'] },

    // پرداخت
    { name: 'stripe',  title: 'Stripe',  purposes: ['payments'], cookies: ['__stripe_mid','__stripe_sid'] },
    { name: 'paypal',  title: 'PayPal',  purposes: ['payments'] },

    // شخصی‌سازی اول‌شخص (اختیاری)
    { name: 'ol-recommendations', title: 'On-site recommendations', purposes: ['personalization'],
      cookies: ['ol_recs_enabled','ol_pref_*'] }
  ],

  translations: {
    en: {
      consentNotice: {
        description:
          'We use cookies to run OpenLibrary and to improve your experience (security, limited analytics, embedded media). You can accept all, reject optional cookies, or customize your choices.'
      },
      consentModal: {
        title: 'Privacy settings',
        description: 'Use the switches below to enable or disable services by category. Required services cannot be turned off.'
      },
      ok: 'Accept selected',
      acceptAll: 'Accept all',
      decline: 'I decline',
      learnMore: 'Let me choose',
      purposes: {
        essential: 'Essential',
        security: 'Security',
        analytics: 'Analytics',
        external: 'External media',
        support: 'Support/Chat',
        payments: 'Payments',
        personalization: 'Personalization'
      },
      app: { required: { title: '(always required)', description: 'These cookies are necessary for the website to function.' } }
    }
  }
};
