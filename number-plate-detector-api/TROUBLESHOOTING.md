# Troubleshooting Guide

## Common Issues

### OpenAI API Error: Client.__init__() got an unexpected keyword argument 'proxies'

**Error Message:**
```
500: OpenAI API error: Client.__init__() got an unexpected keyword argument 'proxies'
```

**Cause:**
This error occurs due to a compatibility issue between the OpenAI Python library and the httpx package. The httpx package version 0.28.0 removed the deprecated 'proxies' argument, but the OpenAI library still uses it in older versions.

**Solution:**
This issue has been fixed by pinning the httpx package to version 0.27.2 in the requirements.txt file. If you encounter this error, make sure your requirements.txt contains:

```
httpx==0.27.2
```

If you're using a local development environment and encounter this error, you can fix it by running:

```bash
pip install httpx==0.27.2 --force-reinstall
```

Alternatively, you can upgrade the OpenAI package to version 1.55.3 or newer, which has been updated to work with newer versions of httpx:

```bash
pip install openai>=1.55.3
```

### OpenAI API Error: Connection error

**Error Message:**
```
500: OpenAI API error: Connection error
```

**Cause:**
This error typically occurs when:
1. The OpenAI API key is missing or invalid
2. The backend cannot connect to the OpenAI API (network issue)
3. The OpenAI API service is experiencing downtime

**Solution:**
1. **Check your API key:**
   - Make sure you have a valid OpenAI API key in your `.env` file:
   ```
   OPENAI_API_KEY=your_actual_openai_api_key
   ```
   - Ensure the API key is being properly passed to the container via environment variables or env_file in docker-compose.yml
   - Verify your API key is valid and has sufficient quota

2. **Check network connectivity:**
   - Make sure your backend container can connect to the internet
   - Check if any proxies or firewalls might be blocking the connection to OpenAI's API

3. **Restart the containers:**
   ```bash
   docker-compose down && docker-compose up -d
   ```

4. **Check OpenAI's status:**
   - Visit [OpenAI Status Page](https://status.openai.com/) to verify if there are any ongoing service disruptions

### How to Get a Valid OpenAI API Key

To use this application, you need a valid OpenAI API key that has access to the GPT-4o Mini model:

1. **Sign up for an OpenAI account:**
   - Visit [OpenAI's website](https://openai.com) and sign up for an account if you don't have one.

2. **Subscribe to a paid plan:**
   - GPT-4o Mini is available on paid plans. Go to [OpenAI API pricing](https://openai.com/pricing) to see the available options.

3. **Generate an API key:**
   - Go to the [API keys page](https://platform.openai.com/api-keys) in your OpenAI account.
   - Click "Create new secret key" and give it a name related to this application.
   - Copy the API key immediately as it won't be shown again.

4. **Set up your API key in the application:**
   - Create a `.env` file in the `number-plate-detector-api` directory with the following content:
   ```
   OPENAI_API_KEY=your_actual_openai_api_key
   ```
   - Or use the provided `setup.sh` script to configure your API key.

5. **Check API key usage and limits:**
   - Monitor your usage on the [OpenAI usage page](https://platform.openai.com/usage) to avoid unexpected charges.
   - Set up usage limits if needed on the [OpenAI billing page](https://platform.openai.com/account/billing/limits). 